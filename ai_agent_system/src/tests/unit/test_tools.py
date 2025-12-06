import pytest
from pydantic import BaseModel

from src.agents.base.tool import BaseTool


class EchoParams(BaseModel):
    text: str


class EchoTool(BaseTool):
    async def _run(self, params: BaseModel):  # type: ignore[override]
        return params.text


@pytest.mark.asyncio
async def test_base_tool_execute():
    tool = EchoTool(name="echo", description="echo", param_model=EchoParams)
    result = await tool.execute(text="hi")
    assert result == "hi"
