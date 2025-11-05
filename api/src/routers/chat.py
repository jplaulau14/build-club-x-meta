import json
import os

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic_ai import Agent

from ..config import settings
from ..schemas import ChatRequest, ChatResponse

router = APIRouter(tags=["chat"])

os.environ["OLLAMA_BASE_URL"] = f"{settings.ollama_host}/v1"

simple_agent = Agent(f"ollama:{settings.model_name}", retries=settings.ai_max_retries)


@simple_agent.system_prompt
def system_prompt(ctx) -> str:
    return (
        ctx.system_prompt
        if hasattr(ctx, "system_prompt")
        else "You are a helpful assistant."
    )


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    result = await simple_agent.run(
        request.message,
        message_history=[],
        model_settings={"temperature": request.temperature},
    )
    return ChatResponse(response=result.data, model=settings.model_name)


async def _stream_chat_response(request: ChatRequest):
    try:
        async with simple_agent.run_stream(
            request.message,
            message_history=[],
            model_settings={"temperature": request.temperature},
        ) as result:
            async for text_delta in result.stream_text(delta=True):
                yield f"data: {json.dumps({'content': text_delta})}\n\n"

            yield f"data: {json.dumps({'done': True})}\n\n"
    except Exception as e:
        error_msg = json.dumps({"error": str(e)})
        yield f"data: {error_msg}\n\n"


@router.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    return StreamingResponse(
        _stream_chat_response(request),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
