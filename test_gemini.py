"""Test Google Gemini integration - run from project root."""

import asyncio
import sys
import os

# Change to ai_agent_system directory
os.chdir('ai_agent_system')
sys.path.insert(0, os.getcwd())

# Load settings first
from src.config.settings import Settings
settings = Settings()
print(f"Loaded GEMINI_API_KEY: {settings.GEMINI_API_KEY[:20] if settings.GEMINI_API_KEY else 'NOT SET'}...")

from src.tools.llm import get_gemini_client


async def test_gemini():
    """Test Gemini API."""
    print("Testing Gemini API...")
    print("-" * 50)
    
    try:
        client = get_gemini_client(model="gemini-2.5-flash")
        
        # Simple generation
        print("\n1. Testing simple content generation...")
        response = await client.generate_content(
            prompt="Write a short poem about AI agents in 4 lines",
            temperature=0.7,
            max_tokens=200,
        )
        
        print("\n✅ Generated text:")
        print(response["text"])
        print(f"\nModel: {response['model']}")
        print(f"Usage: {response.get('usage', {})}")
        
        # Chat example
        print("\n" + "-" * 50)
        print("2. Testing chat conversation...")
        messages = [
            {"role": "user", "content": "Hello, what can you help me with?"},
            {"role": "model", "content": "I can help you with writing, coding, and answering questions!"},
            {"role": "user", "content": "Great! Can you write a hello world in Python?"},
        ]
        
        chat_response = await client.chat(messages=messages, temperature=0.5)
        print("\n✅ Chat response:")
        print(chat_response["text"])
        
        await client.close()
        print("\n" + "=" * 50)
        print("✅ All tests passed!")
        
    except ValueError as e:
        print(f"\n❌ Configuration Error: {e}")
        print("\n💡 Make sure to set GEMINI_API_KEY in your .env file")
        print("   Get your key from: https://makersuite.google.com/app/apikey")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_gemini())
