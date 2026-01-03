"""Research API endpoints."""

from uuid import UUID

from fastapi import APIRouter, HTTPException

from app.models.requests import ResearchRequest
from app.models.responses import ResearchResponse

router = APIRouter()


@router.post("/research", response_model=ResearchResponse)
async def research_topic(request: ResearchRequest) -> ResearchResponse:
    """Research a topic and return findings."""
    # TODO: Implement research service
    return ResearchResponse(
        id="research_placeholder",
        topic=request.topic,
        findings=[],
        sources=[],
    )


@router.get("/research/{research_id}", response_model=ResearchResponse)
async def get_research(research_id: UUID) -> ResearchResponse:
    """Get research session by ID."""
    # TODO: Implement database lookup
    raise HTTPException(status_code=404, detail="Research session not found")
