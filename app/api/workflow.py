"""Blog workflow API endpoints using LangGraph agent."""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from app.agents.blog_agent import run_blog_workflow
from app.db.repositories import BlogPostRepository, ResearchSessionRepository

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


# ============== Blog Post Retrieval Endpoints ==============

@router.get("/blogs")
async def list_blog_posts(
    status: Optional[str] = Query(None, description="Filter by status: draft, completed"),
    niche: Optional[str] = Query(None, description="Filter by niche"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
) -> dict:
    """List all saved blog posts from PostgreSQL."""
    try:
        posts = await BlogPostRepository.list_posts(
            status=status,
            niche=niche,
            limit=limit,
            offset=offset,
        )
        return {
            "posts": posts,
            "count": len(posts),
            "limit": limit,
            "offset": offset,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch posts: {str(e)}")


@router.get("/blogs/{post_id}")
async def get_blog_post(post_id: UUID) -> dict:
    """Get a specific blog post by ID."""
    try:
        post = await BlogPostRepository.get_by_id(post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Blog post not found")
        return post
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch post: {str(e)}")


@router.get("/blogs/slug/{slug}")
async def get_blog_post_by_slug(slug: str) -> dict:
    """Get a blog post by slug."""
    try:
        post = await BlogPostRepository.get_by_slug(slug)
        if not post:
            raise HTTPException(status_code=404, detail="Blog post not found")
        return post
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch post: {str(e)}")


@router.delete("/blogs/{post_id}")
async def delete_blog_post(post_id: UUID) -> dict:
    """Delete a blog post."""
    try:
        success = await BlogPostRepository.delete(post_id)
        if not success:
            raise HTTPException(status_code=404, detail="Blog post not found")
        return {"id": str(post_id), "status": "deleted"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete post: {str(e)}")


# ============== Research Session Endpoints ==============

@router.get("/research/{session_id}")
async def get_research_session(session_id: UUID) -> dict:
    """Get a research session by ID."""
    try:
        session = await ResearchSessionRepository.get_by_id(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Research session not found")
        return session
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch session: {str(e)}")


@router.get("/research/topic/{topic}")
async def search_research_by_topic(
    topic: str,
    limit: int = Query(10, ge=1, le=50),
) -> dict:
    """Search research sessions by topic."""
    try:
        sessions = await ResearchSessionRepository.list_by_topic(topic, limit)
        return {
            "topic": topic,
            "sessions": sessions,
            "count": len(sessions),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to search sessions: {str(e)}")
