import pytest

from src.agents.base.agent import BaseAgent


class EchoAgent(BaseAgent):
    async def act(self, chain_of_thought: str, **kwargs):  # type: ignore[override]
        return chain_of_thought


@pytest.mark.asyncio
async def test_base_agent_execute():
    agent = EchoAgent(name="echo", role="test", capabilities=["echo"])
    result = await agent.execute("hello")
    assert result == "Plan for task: hello"
    assert agent.metrics["invocations"] == 1
