class AgentSystemError(Exception):
    """Base exception for agent system."""


class AgentExecutionError(AgentSystemError):
    """Agent failed to execute task."""


class ToolExecutionError(AgentSystemError):
    """Tool failed during execution."""
