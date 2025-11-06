from fastapi import APIRouter, HTTPException

from ..schemas.extraction import ExtractionRequest, ExtractionResponse
from ..services.extraction_service import extract_structured_data

router = APIRouter(tags=["extraction"])


@router.post("/chat/extract", response_model=ExtractionResponse)
async def extract(request: ExtractionRequest):
    try:
        extracted_data = await extract_structured_data(
            request.text, request.schema_name
        )
        return ExtractionResponse(
            data=extracted_data.model_dump(), schema_used=request.schema_name
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Extraction failed: {str(e)}"
        )
