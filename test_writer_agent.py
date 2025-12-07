"""Test WriterAgent with Gemini."""

import asyncio
import sys
import os

os.chdir('ai_agent_system')
sys.path.insert(0, os.getcwd())

# Load settings
from src.config.settings import Settings
settings = Settings()
print(f"Loaded GEMINI_API_KEY: {settings.GEMINI_API_KEY[:20] if settings.GEMINI_API_KEY else 'NOT SET'}...\n")

from src.agents.specialized import WriterAgent
from src.agents.base.memory import ShortTermMemory


async def test_writer_agent():
    """Test WriterAgent using Gemini."""
    print("Testing WriterAgent with Gemini...")
    print("=" * 60)
    
    # Create agent
    agent = WriterAgent(
        name="ContentWriter",
        role="Content generation specialist",
        capabilities=["content_generation", "creative_writing", "code_generation"],
        memory=ShortTermMemory()
    )
    
    # Test 1: Simple generation
    print("\n1. Simple content generation:")
    print("-" * 60)
    result = await agent.act(
        chain_of_thought="Generate content",
        prompt="Write a professional introduction for an AI agent system"
    )
    print(result)
    
    # Test 2: With system instruction
    print("\n\n2. With system instruction:")
    print("-" * 60)
    result2 = await agent.act(
        chain_of_thought="Generate code",
        prompt="Write a Python function to reverse a string",
        system_instruction="You are a Python expert. Write clean, documented code."
    )
    print(result2)
    
    # Check memory
    print("\n\n3. Agent memory:")
    print("-" * 60)
    recent = await agent.memory.get_recent(limit=5)
    print(f"Memory entries: {len(recent)}")
    for i, memory in enumerate(recent, 1):
        print(f"\nEntry {i}:")
        print(f"  Content: {str(memory)[:150]}...")
    
    print("\n" + "=" * 60)
    print("✅ WriterAgent test complete!")


if __name__ == "__main__":
    asyncio.run(test_writer_agent())
