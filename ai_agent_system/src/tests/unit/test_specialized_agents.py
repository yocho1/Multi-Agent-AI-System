import pytest

from src.agents.specialized import WriterAgent, FlightAgent, WeatherAgent, CodeAgent


@pytest.mark.asyncio
async def test_writer_agent():
    agent = WriterAgent(name="writer", role="Content Generator", capabilities=["write"])
    result = await agent.execute("Generate intro", prompt="Hello world")
    assert "Generated content for" in result
    assert agent.metrics["invocations"] == 1


@pytest.mark.asyncio
async def test_flight_agent():
    agent = FlightAgent(name="flight", role="Flight Booker", capabilities=["search", "book"])
    result = await agent.execute("Find flights", origin="LAX", destination="JFK")
    assert result["origin"] == "LAX"
    assert result["destination"] == "JFK"
    assert len(result["flights"]) > 0


@pytest.mark.asyncio
async def test_weather_agent():
    agent = WeatherAgent(name="weather", role="Weather Checker", capabilities=["forecast"])
    result = await agent.execute("Check weather", location="NYC")
    assert result["location"] == "NYC"
    assert "temperature" in result
    assert "condition" in result


@pytest.mark.asyncio
async def test_code_agent():
    agent = CodeAgent(name="code", role="Code Generator", capabilities=["generate", "execute"])
    result = await agent.execute("Generate code", code_task="write a function")
    assert result["task"] == "write a function"
    assert "generated_code" in result
