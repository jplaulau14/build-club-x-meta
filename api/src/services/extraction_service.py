import os

from pydantic import BaseModel
from pydantic_ai import Agent

from ..config import settings
from ..data.extraction_schemas import get_schema_metadata
from ..schemas.extraction import get_schema

os.environ["OLLAMA_BASE_URL"] = f"{settings.ollama_host}/v1"


async def extract_structured_data(
    text: str,
    schema_name: str,
) -> BaseModel:
    schema_model = get_schema(schema_name)
    if not schema_model:
        raise ValueError(f"Unknown schema: {schema_name}")

    metadata = get_schema_metadata(schema_name)
    system_prompt = (
        metadata["system_prompt"]
        if metadata
        else f"Extract {schema_name} information from the given text. Be thorough and accurate. Only extract information that is explicitly mentioned in the text."
    )

    extraction_agent = Agent(
        f"ollama:{settings.model_name}",
        result_type=schema_model,
        retries=settings.ai_max_retries,
        system_prompt=system_prompt,
    )

    result = await extraction_agent.run(text)

    return result.output
