import os
from dataclasses import dataclass
from typing import AsyncGenerator

from pydantic_ai import Agent

from ..config import settings

os.environ["OLLAMA_BASE_URL"] = f"{settings.ollama_host}/v1"


@dataclass
class PersonaDeps:
    system_prompt: str


persona_agent = Agent(
    f"ollama:{settings.model_name}",
    deps_type=PersonaDeps,
    retries=settings.ai_max_retries,
)


@persona_agent.system_prompt
def get_system_prompt(ctx) -> str:
    return ctx.deps.system_prompt


async def chat_with_persona(
    system_prompt: str,
    message: str,
    temperature: float = 0.7,
) -> str:
    """Chat with a persona using custom system prompt."""
    deps = PersonaDeps(system_prompt=system_prompt)

    result = await persona_agent.run(
        message,
        deps=deps,
        message_history=[],
        model_settings={"temperature": temperature},
    )

    return result.output


async def stream_with_persona(
    system_prompt: str,
    message: str,
    temperature: float = 0.7,
) -> AsyncGenerator[str, None]:
    """Stream chat responses with a persona using custom system prompt."""
    deps = PersonaDeps(system_prompt=system_prompt)

    async with persona_agent.run_stream(
        message,
        deps=deps,
        message_history=[],
        model_settings={"temperature": temperature},
    ) as result:
        async for text_delta in result.stream_text(delta=True):
            yield text_delta
