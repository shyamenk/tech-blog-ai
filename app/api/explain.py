"""Concept explanation API endpoints."""

from fastapi import APIRouter, HTTPException

from app.models.requests import ExplainRequest
from app.models.responses import ExplainResponse
from app.services.content_service import get_content_service

router = APIRouter()


@router.post("/explain", response_model=ExplainResponse)
async def explain_concept(request: ExplainRequest) -> ExplainResponse:
    """Explain a technical concept using AI."""
    try:
        content_service = get_content_service()
        result = await content_service.explain_concept(
            concept=request.concept,
            mode=request.mode,
            include_examples=request.include_examples,
            include_analogies=request.include_analogies,
        )

        return ExplainResponse(
            concept=result.get("concept", request.concept),
            explanation=result.get("explanation", ""),
            examples=result.get("examples", []),
            analogies=result.get("analogies", []),
            mode=result.get("mode", request.mode),
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to explain concept: {str(e)}")
