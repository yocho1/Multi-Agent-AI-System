"""Test Google Gemini integration."""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from ai_agent_system.src.tools.llm import get_gemini_client


async def test_gemini():
    """Test Gemini API."""
    client = get_gemini_client(model="gemini-pro")
    
    # Simple generation
    response = await client.generate_content(
        prompt="Write a short poem about AI agents",
        temperature=0.7,
        max_tokens=200,
    )
    
    print("Generated text:")
    print(response["text"])
    print(f"\nModel: {response['model']}")
    print(f"Usage: {response.get('usage', {})}")
    
    # Chat example
    messages = [
        {"role": "user", "content": "Hello, what is your name?"},
        {"role": "model", "content": "I am Gemini, Google's AI assistant."},
        {"role": "user", "content": "Can you help me write code?"},
    ]
    
    chat_response = await client.chat(messages=messages, temperature=0.5)
    print("\n\nChat response:")
    print(chat_response["text"])
    
    await client.close()


if __name__ == "__main__":
    asyncio.run(test_gemini())
