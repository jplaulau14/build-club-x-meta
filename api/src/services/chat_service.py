import json
import os
from typing import AsyncGenerator

from pydantic_ai import Agent
from pydantic_ai.messages import ModelMessage

from ..config import settings

os.environ["OLLAMA_BASE_URL"] = f"{settings.ollama_host}/v1"

chat_agent = Agent(f"ollama:{settings.model_name}", retries=settings.ai_max_retries)


@chat_agent.system_prompt
def system_prompt() -> str:
    return "You are a helpful assistant."


async def chat(
    message: str,
    temperature: float = 0.7,
    message_history: list[ModelMessage] | None = None,
) -> str:
    result = await chat_agent.run(
        message,
        message_history=message_history or [],
        model_settings={"temperature": temperature},
    )
    return result.output


async def chat_stream(
    message: str,
    temperature: float = 0.7,
    message_history: list[ModelMessage] | None = None,
) -> AsyncGenerator[str, None]:
    try:
        async with chat_agent.run_stream(
            message,
            message_history=message_history or [],
            model_settings={"temperature": temperature},
        ) as result:
            async for text_delta in result.stream_text(delta=True):
                yield f"data: {json.dumps({'content': text_delta})}\n\n"

            yield f"data: {json.dumps({'done': True})}\n\n"
    except Exception as e:
        error_msg = json.dumps({"error": str(e)})
        yield f"data: {error_msg}\n\n"
