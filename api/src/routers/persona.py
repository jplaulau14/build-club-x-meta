import json
from typing import AsyncGenerator

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from ..agents.persona_agent import stream_with_persona
from ..config import settings
from ..data.personas import get_persona, list_personas
from ..schemas import PersonaRequest

router = APIRouter(tags=["persona"])


async def _stream_persona_chat(request: PersonaRequest) -> AsyncGenerator[str, None]:
    try:
        if request.custom_system_prompt:
            system_prompt = request.custom_system_prompt
            persona_name = "Custom"
        else:
            persona = get_persona(request.persona_name)
            system_prompt = persona.system_prompt
            persona_name = persona.name

        yield f"data: {json.dumps({'persona': persona_name, 'model': settings.model_name})}\n\n"

        async for text_delta in stream_with_persona(
            system_prompt=system_prompt,
            message=request.message,
            temperature=request.temperature,
        ):
            yield f"data: {json.dumps({'content': text_delta})}\n\n"

        yield f"data: {json.dumps({'done': True})}\n\n"
    except Exception as e:
        error_msg = json.dumps({"error": str(e)})
        yield f"data: {error_msg}\n\n"


@router.post("/chat/persona")
async def chat_persona(request: PersonaRequest):
    return StreamingResponse(
        _stream_persona_chat(request),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@router.get("/personas")
async def get_personas():
    return list_personas()
