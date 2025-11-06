import os

from pydantic import BaseModel
from pydantic_ai import Agent

from ..config import settings
from ..schemas.extraction import get_schema

os.environ["OLLAMA_BASE_URL"] = f"{settings.ollama_host}/v1"


async def extract_structured_data(
    text: str,
    schema_name: str,
) -> BaseModel:
    schema_model = get_schema(schema_name)
    if not schema_model:
        raise ValueError(f"Unknown schema: {schema_name}")

    extraction_agent = Agent(
        f"ollama:{settings.model_name}",
        result_type=schema_model,
        retries=settings.ai_max_retries,
        system_prompt=f"Extract {schema_name} information from the given text. Be thorough and accurate. Only extract information that is explicitly mentioned in the text.",
    )

    result = await extraction_agent.run(text)

    return result.output
