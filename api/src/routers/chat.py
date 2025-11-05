import json
from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from ..config import settings
from ..core.chats import ChatManager
from ..core.dependencies import get_current_user
from ..database.database import get_db
from ..database.models import User
from ..schemas import ChatRequest, ChatResponse
from ..services import chat_service, memory_chat_service

router = APIRouter(tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    response = await chat_service.chat(request.message, request.temperature)
    return ChatResponse(response=response, model=settings.model_name)


@router.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    return StreamingResponse(
        chat_service.chat_stream(request.message, request.temperature),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


async def _stream_memory_chat(
    request: ChatRequest,
    chat_id: str,
    db: AsyncSession,
):
    message_history = await memory_chat_service.get_message_history(chat_id, db)

    full_response = ""
    async for chunk in chat_service.chat_stream(
        request.message,
        request.temperature,
        message_history,
    ):
        if chunk.startswith("data: "):
            try:
                data = json.loads(chunk[6:].strip())
                if "content" in data:
                    full_response += data["content"]
            except json.JSONDecodeError:
                pass

        yield chunk

    manager = ChatManager(db)
    await manager.add_message(chat_id, "user", request.message)
    await manager.add_message(chat_id, "assistant", full_response)


@router.post("/chat/memory")
async def chat_memory(
    request: ChatRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    x_chat_id: Annotated[str, Header()],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    manager = ChatManager(db)
    chat = await manager.get_chat(x_chat_id)
    if not chat or chat.user_id != current_user.id:
        raise HTTPException(401, "Invalid chat")

    return StreamingResponse(
        _stream_memory_chat(request, x_chat_id, db),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
