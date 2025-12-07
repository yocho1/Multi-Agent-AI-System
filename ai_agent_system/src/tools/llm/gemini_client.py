"""Google Gemini API client for LLM interactions."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

import google.generativeai as genai
from tenacity import retry, stop_after_attempt, wait_exponential

from src.config.settings import settings
from src.config.logging_config import get_logger

logger = get_logger(component="gemini_client")


class GeminiClient:
    """Client for Google Gemini API using official SDK."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gemini-2.5-flash",
        timeout: float = 60.0,
    ):
        """Initialize Gemini client.
        
        Args:
            api_key: Gemini API key (defaults to settings)
            model: Model name to use (gemini-pro, gemini-1.5-flash, etc.)
            timeout: Request timeout in seconds
        """
        self.api_key = api_key or settings.GEMINI_API_KEY
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in settings or provided")
        
        # Configure the SDK
        genai.configure(api_key=self.api_key)
        
        self.model_name = model
        self.timeout = timeout
        
        # Configure safety settings to be more permissive
        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE",
            },
        ]
        
        self.model = genai.GenerativeModel(
            model,
            safety_settings=safety_settings
        )
        
        logger.info(
            "Gemini client initialized",
            model=model,
        )

    async def close(self):
        """Close the client (no-op for SDK)."""
        pass

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True,
    )
    async def generate_content(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Generate content using Gemini API.
        
        Args:
            prompt: The prompt to generate from
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens to generate
            **kwargs: Additional parameters for the API
            
        Returns:
            Dict containing the generated text and metadata
        """
        try:
            # Configure generation parameters
            generation_config = {
                "temperature": temperature,
            }
            if max_tokens:
                generation_config["max_output_tokens"] = max_tokens
            
            # Extract system_instruction if provided
            # (not part of generation_config)
            kwargs.pop("system_instruction", None)

            generation_config.update(kwargs)
            
            # Generate content
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            # Handle safety filtering and empty responses
            text = ""
            if hasattr(response, 'text'):
                try:
                    text = response.text
                except ValueError as e:
                    # Safety filter or empty response
                    logger.warning(
                        "Response text unavailable",
                        error=str(e),
                        finish_reason=getattr(
                            response.candidates[0]
                            if response.candidates else None,
                            'finish_reason',
                            'unknown'
                        )
                    )
                    if response.candidates and response.candidates[0].content.parts:
                        # Try to get text from parts directly
                        text = "".join(
                            part.text
                            for part in response.candidates[0].content.parts
                            if hasattr(part, 'text')
                        )
            
            if not text:
                # Return empty text with safety info
                text = ""
            
            logger.info(
                "Content generated successfully",
                model=self.model_name,
                prompt_length=len(prompt),
                response_length=len(text),
            )
            
            return {
                "text": text,
                "model": self.model_name,
                "usage": {
                    "prompt_tokens": getattr(response, "prompt_token_count", 0),
                    "completion_tokens": getattr(response, "candidates_token_count", 0) if hasattr(response, "candidates_token_count") else 0,
                },
            }
            
        except Exception as e:
            logger.error(
                "Gemini API request failed",
                error=str(e),
                error_type=type(e).__name__,
            )
            raise

    async def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Have a conversation using Gemini API.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens to generate
            **kwargs: Additional parameters
            
        Returns:
            Dict containing the response and metadata
        """
        try:
            # Configure generation parameters
            generation_config = {
                "temperature": temperature,
            }
            if max_tokens:
                generation_config["max_output_tokens"] = max_tokens
            
            generation_config.update(kwargs)
            
            # Start chat session
            chat = self.model.start_chat(history=[])
            
            # Add all but last message to history
            for msg in messages[:-1]:
                role = "user" if msg["role"] == "user" else "model"
                chat.history.append({
                    "role": role,
                    "parts": [msg["content"]]
                })
            
            # Send last message
            last_message = messages[-1]["content"]
            response = chat.send_message(
                last_message,
                generation_config=generation_config
            )
            
            text = response.text if response.text else ""
            
            logger.info(
                "Chat response generated",
                model=self.model_name,
                message_count=len(messages),
                response_length=len(text),
            )
            
            return {
                "text": text,
                "model": self.model_name,
                "usage": {
                    "prompt_tokens": getattr(response, "prompt_token_count", 0),
                    "completion_tokens": getattr(response, "candidates_token_count", 0) if hasattr(response, "candidates_token_count") else 0,
                },
            }
            
        except Exception as e:
            logger.error(
                "Gemini chat request failed",
                error=str(e),
                error_type=type(e).__name__,
            )
            raise


# Global client instance
_gemini_client: Optional[GeminiClient] = None


def get_gemini_client(model: str = "gemini-2.5-flash") -> GeminiClient:
    """Get or create global Gemini client instance.
    
    Args:
        model: Model name to use
        
    Returns:
        GeminiClient instance
    """
    global _gemini_client
    if _gemini_client is None:
        _gemini_client = GeminiClient(model=model)
    return _gemini_client


async def close_gemini_client() -> None:
    """Close global Gemini client."""
    global _gemini_client
    if _gemini_client:
        await _gemini_client.close()
        _gemini_client = None
