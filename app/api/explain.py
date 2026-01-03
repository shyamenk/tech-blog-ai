"""Concept explanation API endpoints."""

from fastapi import APIRouter

from app.models.requests import ExplainRequest
from app.models.responses import ExplainResponse

router = APIRouter()


@router.post("/explain", response_model=ExplainResponse)
async def explain_concept(request: ExplainRequest) -> ExplainResponse:
    """Explain a technical concept."""
    # TODO: Implement explanation service
    return ExplainResponse(
        concept=request.concept,
        explanation="",
        examples=[],
        analogies=[],
        mode=request.mode,
    )
