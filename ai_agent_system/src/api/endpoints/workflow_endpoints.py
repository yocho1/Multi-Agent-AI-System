from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/workflows", tags=["workflows"])


class WorkflowExecuteRequest(BaseModel):
    workflow_id: str
    input: Dict[str, Any]


@router.post("/execute", summary="Execute a workflow")
async def execute_workflow(payload: WorkflowExecuteRequest) -> Dict[str, Any]:
    # Placeholder: would trigger orchestrator to run workflow graph
    return {"workflow_id": payload.workflow_id, "status": "accepted", "input": payload.input}
