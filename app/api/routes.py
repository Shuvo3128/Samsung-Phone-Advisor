from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.schemas import AskRequest, AskResponse
from app.core.database import get_db
from app.agents.agent_manager import AgentManager

router = APIRouter()


@router.post("/ask", response_model=AskResponse)
async def ask_question(
    request: AskRequest,
    db: Session = Depends(get_db)
):
    manager = AgentManager(db)

    result = await manager.handle(request.question)

    return AskResponse(
        answer=result["answer"],
        confidence=result.get("confidence"),
        intent=result.get("intent"),
        latency_ms=result.get("latency_ms"),
    )
