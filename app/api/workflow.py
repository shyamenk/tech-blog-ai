"""Blog workflow API endpoints using LangGraph agent."""

from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.agents.blog_agent import run_blog_workflow

router = APIRouter()


class BlogWorkflowRequest(BaseModel):
    """Request model for blog workflow."""

    topic: str = Field(..., min_length=3, max_length=500, description="Blog post topic")
    niche: Optional[str] = Field(None, description="Content niche (salesforce, fullstack, ai)")
    target_audience: str = Field(
        "intermediate", description="Target audience: beginner, intermediate, advanced"
    )
    word_count: int = Field(2000, ge=500, le=10000, description="Target word count")
    tone: str = Field(
        "conversational", description="Writing tone: conversational, formal, tutorial"
    )
    include_code_examples: bool = Field(True, description="Include code examples")


class BlogWorkflowResponse(BaseModel):
    """Response model for blog workflow."""

    status: str
    topic: str
    messages: list[str]
    research: Optional[dict] = None
    outline: Optional[dict] = None
    draft: Optional[dict] = None
    final_content: Optional[dict] = None
    seo_metadata: Optional[dict] = None
    error: Optional[str] = None


@router.post("/workflow/blog", response_model=BlogWorkflowResponse)
async def create_blog_post(request: BlogWorkflowRequest) -> BlogWorkflowResponse:
    """
    Create a complete blog post using the LangGraph workflow.

    This endpoint runs a multi-step AI workflow:
    1. Research - Gathers information about the topic
    2. Outline - Creates a structured outline
    3. Draft - Writes the full blog post
    4. Review - Reviews content quality
    5. Optimize - SEO optimization

    The workflow may take 1-2 minutes to complete.
    """
    try:
        result = await run_blog_workflow(
            topic=request.topic,
            niche=request.niche,
            target_audience=request.target_audience,
            word_count=request.word_count,
            tone=request.tone,
            include_code_examples=request.include_code_examples,
        )

        return BlogWorkflowResponse(
            status=result.get("status", "unknown"),
            topic=result.get("topic", request.topic),
            messages=result.get("messages", []),
            research=result.get("research"),
            outline=result.get("outline"),
            draft=result.get("draft"),
            final_content=result.get("final_content"),
            seo_metadata=result.get("seo_metadata"),
            error=result.get("error"),
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Blog workflow failed: {str(e)}",
        )


@router.get("/workflow/status")
async def workflow_status() -> dict:
    """Get workflow service status."""
    return {
        "service": "blog_workflow",
        "status": "available",
        "steps": ["research", "outline", "draft", "review", "optimize"],
        "description": "Multi-step AI workflow for complete blog post generation",
    }
