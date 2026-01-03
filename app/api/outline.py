"""Outline generation API endpoints."""

from fastapi import APIRouter

from app.models.requests import OutlineRequest
from app.models.responses import OutlineResponse

router = APIRouter()


@router.post("/outline", response_model=OutlineResponse)
async def generate_outline(request: OutlineRequest) -> OutlineResponse:
    """Generate a blog post outline."""
    # TODO: Implement outline generation service
    return OutlineResponse(
        id="outline_placeholder",
        title=f"Guide to {request.topic}",
        hook="",
        sections=[],
        estimated_words=request.word_count,
        seo_suggestions={},
    )
