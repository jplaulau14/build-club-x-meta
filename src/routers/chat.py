import json

import httpx
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from ..config import settings
from ..schemas import ChatRequest, ChatResponse
from ..services.ollama import OllamaService

router = APIRouter(tags=["chat"])
ollama_service = OllamaService()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        response = await ollama_service.chat(request)
        return ChatResponse(response=response, model=settings.model_name)
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Request to Ollama timed out")
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code, detail=f"Ollama API error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    async def generate():
        try:
            async for chunk in ollama_service.chat_stream(request):
                yield f"data: {chunk}\n\n"
        except httpx.TimeoutException:
            error_msg = json.dumps({"error": "Request to Ollama timed out"})
            yield f"data: {error_msg}\n\n"
        except httpx.HTTPStatusError as e:
            error_msg = json.dumps({"error": f"Ollama API error: {str(e)}"})
            yield f"data: {error_msg}\n\n"
        except Exception as e:
            error_msg = json.dumps({"error": f"Internal server error: {str(e)}"})
            yield f"data: {error_msg}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@router.get("/models")
async def list_models():
    try:
        return await ollama_service.list_models()
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Failed to fetch models: {str(e)}")


@router.get("/health")
async def health_check():
    try:
        available_models = await ollama_service.health_check()
        return {
            "status": "healthy",
            "ollama_host": settings.ollama_host,
            "model": settings.model_name,
            "available_models": available_models,
        }
    except Exception as e:
        raise HTTPException(
            status_code=503, detail=f"Ollama service unavailable: {str(e)}"
        )
