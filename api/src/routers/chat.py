import json
from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from ..agents.chat_agent import chat_agent
from ..agents.dependencies import ChatDeps
from ..config import settings
from ..core.dependencies import get_current_user
from ..core.sessions import SessionManager
from ..database.database import get_db
from ..database.models import User
from ..schemas import ChatRequest, ChatResponse

router = APIRouter(tags=["chat"])


async def _validate_session(session_id: str, user: User, db: AsyncSession) -> None:
    manager = SessionManager(db)
    session = await manager.get_session(session_id)
    if not session or session.user_id != user.id:
        raise HTTPException(401, "Invalid session")


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    x_session_id: Annotated[str, Header()],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    await _validate_session(x_session_id, current_user, db)

    deps = ChatDeps(
        db_session=db,
        session_id=x_session_id,
        user_id=current_user.id,
        temperature=request.temperature,
    )

    result = await chat_agent.run(request.message, deps=deps)

    manager = SessionManager(db)
    await manager.add_message(x_session_id, "user", request.message)
    await manager.add_message(x_session_id, "assistant", result.output)

    return ChatResponse(response=result.output, model=settings.model_name)


async def _stream_chat_response(
    request: ChatRequest,
    current_user: User,
    x_session_id: str,
    db: AsyncSession,
):
    try:
        await _validate_session(x_session_id, current_user, db)

        deps = ChatDeps(
            db_session=db,
            session_id=x_session_id,
            user_id=current_user.id,
            temperature=request.temperature,
        )

        async with chat_agent.run_stream(request.message, deps=deps) as result:
            async for text_delta in result.stream_text(delta=True):
                yield f"data: {json.dumps({'content': text_delta})}\n\n"

            yield f"data: {json.dumps({'done': True})}\n\n"

        manager = SessionManager(db)
        await manager.add_message(x_session_id, "user", request.message)
        await manager.add_message(x_session_id, "assistant", result.output)

    except Exception as e:
        error_msg = json.dumps({"error": str(e)})
        yield f"data: {error_msg}\n\n"


@router.post("/chat/stream")
async def chat_stream(
    request: ChatRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    x_session_id: Annotated[str, Header()],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return StreamingResponse(
        _stream_chat_response(request, current_user, x_session_id, db),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
