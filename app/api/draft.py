"""Draft writing API endpoints."""

from fastapi import APIRouter

from app.models.requests import DraftRequest
from app.models.responses import DraftResponse

router = APIRouter()


@router.post("/draft", response_model=DraftResponse)
async def generate_draft(request: DraftRequest) -> DraftResponse:
    """Generate a full blog post draft."""
    # TODO: Implement draft generation service
    return DraftResponse(
        id="draft_placeholder",
        title="",
        content="",
        word_count=0,
        metadata={},
    )
