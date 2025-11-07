from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from ..schemas import ChatRequest
from ..services import github_service

router = APIRouter(prefix="/github", tags=["github"])

@router.post("/chat")
async def github_chat(request: ChatRequest):
    return StreamingResponse(
        github_service.github_chat_stream(
            message=request.message,
            temperature=request.temperature
        ),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )