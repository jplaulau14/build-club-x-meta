import os

from pydantic_ai import Agent

from ..config import settings
from .dependencies import ChatDeps

os.environ["OLLAMA_BASE_URL"] = f"{settings.ollama_host}/v1"

chat_agent = Agent(
    f"ollama:{settings.model_name}",
    deps_type=ChatDeps,
    retries=settings.ai_max_retries,
)


@chat_agent.system_prompt
def system_prompt() -> str:
    return "You are a helpful assistant."
