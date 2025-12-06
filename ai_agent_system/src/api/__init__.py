from fastapi import APIRouter

from src.api.endpoints.agent_endpoints import router as agent_router
from src.api.endpoints.workflow_endpoints import router as workflow_router
from src.api.endpoints.tool_endpoints import router as tool_router
from src.api.endpoints.auth_endpoints import router as auth_router

router = APIRouter(prefix="/api/v1")
router.include_router(auth_router)
router.include_router(agent_router)
router.include_router(workflow_router)
router.include_router(tool_router)

__all__ = ["router"]
