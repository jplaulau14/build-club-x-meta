from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from ..config import settings
from ..schemas import ChatRequest, ChatResponse
from ..services import chat_service

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
