"""Research API endpoints."""

from uuid import UUID

from fastapi import APIRouter, HTTPException

from app.models.requests import ResearchRequest
from app.models.responses import ResearchResponse, ResearchFinding
from app.services.research_service import get_research_service

router = APIRouter()


@router.post("/research", response_model=ResearchResponse)
async def research_topic(request: ResearchRequest) -> ResearchResponse:
    """Research a topic and return findings using AI."""
    try:
        research_service = get_research_service()
        result = await research_service.research_topic(
            topic=request.topic,
            niche=request.niche,
            depth=request.depth,
        )

        # Convert findings to proper format
        findings = []
        for finding in result.get("findings", []):
            if isinstance(finding, dict):
                findings.append(
                    ResearchFinding(
                        title=finding.get("title", ""),
                        content=finding.get("content", ""),
                        confidence=finding.get("confidence", 0.8),
                        source=finding.get("source"),
                    )
                )

        return ResearchResponse(
            id=result.get("id", "research_unknown"),
            topic=result.get("topic", request.topic),
            findings=findings,
            sources=result.get("sources", []),
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to research topic: {str(e)}")


@router.get("/research/{research_id}", response_model=ResearchResponse)
async def get_research(research_id: UUID) -> ResearchResponse:
    """Get research session by ID."""
    # TODO: Implement database lookup
    raise HTTPException(status_code=404, detail="Research session not found")
