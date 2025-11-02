import json
from typing import Annotated

import httpx
from fastapi import APIRouter, Depends, Header, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from ..config import settings
from ..core.dependencies import get_current_user
from ..core.sessions import SessionManager
from ..database.database import get_db
from ..database.models import User
from ..schemas import ChatRequest, ChatResponse
from ..services.ollama import OllamaService

router = APIRouter(tags=["chat"])
ollama_service = OllamaService()


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    x_session_id: Annotated[str, Header()],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    try:
        manager = SessionManager(db)

        messages = await manager.get_session_messages(x_session_id)
        message_history = [
            {"role": msg.role, "content": msg.content} for msg in messages
        ]

        full_messages = [{"role": "system", "content": request.system_prompt}]
        full_messages.extend(message_history)
        full_messages.append({"role": "user", "content": request.message})

        assistant_response = await ollama_service.chat_with_history(
            full_messages, request.temperature
        )

        await manager.add_message(x_session_id, "user", request.message)
        await manager.add_message(x_session_id, "assistant", assistant_response)

        return ChatResponse(response=assistant_response, model=settings.model_name)
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Request to Ollama timed out")
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code, detail=f"Ollama API error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/chat/stream")
async def chat_stream(
    request: ChatRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    x_session_id: Annotated[str, Header()],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    async def generate():
        full_response = ""
        try:
            manager = SessionManager(db)

            messages = await manager.get_session_messages(x_session_id)
            message_history = [
                {"role": msg.role, "content": msg.content} for msg in messages
            ]

            full_messages = [{"role": "system", "content": request.system_prompt}]
            full_messages.extend(message_history)
            full_messages.append({"role": "user", "content": request.message})

            async for chunk in ollama_service.chat_stream_with_history(
                full_messages, request.temperature
            ):
                chunk_data = json.loads(chunk)
                if "content" in chunk_data:
                    full_response += chunk_data["content"]
                yield f"data: {chunk}\n\n"

            await manager.add_message(x_session_id, "user", request.message)
            await manager.add_message(x_session_id, "assistant", full_response)

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
