import os
import logging

from pydantic import BaseModel, ValidationError
from pydantic_ai import Agent

from ..config import settings
from ..data.extraction_schemas import get_schema_metadata
from ..schemas.extraction import get_schema

os.environ["OLLAMA_BASE_URL"] = f"{settings.ollama_host}/v1"

logger = logging.getLogger(__name__)


async def extract_structured_data(
    text: str,
    schema_name: str,
) -> BaseModel:
    print(f"\n=== Starting extraction for schema: {schema_name} ===")
    logger.info(f"Starting extraction for schema: {schema_name}")

    schema_model = get_schema(schema_name)
    if not schema_model:
        raise ValueError(f"Unknown schema: {schema_name}")

    metadata = get_schema_metadata(schema_name)
    system_prompt = (
        metadata["system_prompt"]
        if metadata
        else f"Extract {schema_name} information from the given text. Be thorough and accurate. Only extract information that is explicitly mentioned in the text."
    )

    print(f"System prompt length: {len(system_prompt)} chars")
    print(f"Input text: {text[:100]}...")

    extraction_agent = Agent(
        f"ollama:{settings.model_name}",
        output_type=schema_model,
        retries=settings.ai_max_retries,
        system_prompt=system_prompt,
    )

    # Enable debug logging for pydantic-ai
    import logging as stdlib_logging
    pydantic_logger = stdlib_logging.getLogger("pydantic_ai")
    pydantic_logger.setLevel(stdlib_logging.DEBUG)

    try:
        print("Calling agent.run()...")
        logger.info("Calling agent.run()...")
        result = await extraction_agent.run(text)
        print("Agent completed successfully!")
        print(f"Result type: {type(result.output)}")
        print(f"Result data: {result.output}")
        logger.info("Agent completed successfully")
        return result.output
    except ValidationError as e:
        print("\n!!! VALIDATION ERROR !!!")
        print(f"Error details: {e}")
        print(f"Errors: {e.errors()}")
        logger.error(f"Validation error: {e.errors()}")
        raise
    except Exception as e:
        print("\n!!! UNEXPECTED ERROR !!!")
        print(f"Error type: {type(e)}")
        print(f"Error message: {str(e)}")
        if hasattr(e, '__cause__'):
            print(f"Cause: {e.__cause__}")
        logger.error(f"Extraction error: {str(e)}")
        raise
