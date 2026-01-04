"""LangGraph Blog Creation Agent - Multi-step workflow for blog generation."""

from typing import TypedDict, Optional, Annotated
from operator import add
from uuid import UUID

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from app.services.llm_service import get_llm_service
from app.services.content_service import get_content_service
from app.services.research_service import get_research_service
from app.db.repositories import BlogPostRepository, ResearchSessionRepository


class BlogState(TypedDict):
    """State schema for the blog creation workflow."""

    # Input
    topic: str
    niche: Optional[str]
    target_audience: str
    word_count: int
    tone: str
    include_code_examples: bool

    # Workflow state
    current_step: str
    messages: Annotated[list[str], add]

    # Research output
    research_findings: Optional[dict]

    # Outline output
    outline: Optional[dict]

    # Draft output
    draft: Optional[dict]

    # Review output
    review_feedback: Optional[str]
    needs_revision: bool
    revision_count: int

    # Final output
    final_content: Optional[dict]
    seo_metadata: Optional[dict]

    # Status
    status: str
    error: Optional[str]


async def research_node(state: BlogState) -> dict:
    """Research node - Gathers information about the topic."""
    try:
        research_service = get_research_service()

        findings = await research_service.research_topic(
            topic=state["topic"],
            niche=state.get("niche"),
            depth="medium",
        )

        return {
            "research_findings": findings,
            "current_step": "research_complete",
            "messages": [f"Research completed: Found {len(findings.get('findings', []))} findings"],
            "status": "in_progress",
        }
    except Exception as e:
        return {
            "error": f"Research failed: {str(e)}",
            "status": "failed",
            "messages": [f"Research failed: {str(e)}"],
        }


async def outline_node(state: BlogState) -> dict:
    """Outline node - Creates blog post structure."""
    try:
        content_service = get_content_service()

        outline = await content_service.generate_outline(
            topic=state["topic"],
            niche=state.get("niche"),
            target_audience=state.get("target_audience", "intermediate"),
            word_count=state.get("word_count", 2000),
            include_code_examples=state.get("include_code_examples", True),
        )

        return {
            "outline": outline,
            "current_step": "outline_complete",
            "messages": [f"Outline created: {len(outline.get('sections', []))} sections"],
            "status": "in_progress",
        }
    except Exception as e:
        return {
            "error": f"Outline generation failed: {str(e)}",
            "status": "failed",
            "messages": [f"Outline failed: {str(e)}"],
        }


async def draft_node(state: BlogState) -> dict:
    """Draft node - Writes the full blog post."""
    try:
        content_service = get_content_service()

        draft = await content_service.generate_draft(
            topic=state["topic"],
            outline=state.get("outline"),
            tone=state.get("tone", "conversational"),
            word_count=state.get("word_count", 2000),
            include_code_examples=state.get("include_code_examples", True),
        )

        return {
            "draft": draft,
            "current_step": "draft_complete",
            "messages": [f"Draft written: {draft.get('word_count', 0)} words"],
            "status": "in_progress",
        }
    except Exception as e:
        return {
            "error": f"Draft generation failed: {str(e)}",
            "status": "failed",
            "messages": [f"Draft failed: {str(e)}"],
        }


async def review_node(state: BlogState) -> dict:
    """Review node - Reviews the draft for quality."""
    try:
        llm_service = get_llm_service()

        draft_content = state.get("draft", {}).get("content", "")

        review_prompt = f"""Review this blog post draft and provide feedback:

Title: {state.get('draft', {}).get('title', 'Untitled')}
Topic: {state['topic']}
Target Audience: {state.get('target_audience', 'intermediate')}

Content:
{draft_content[:3000]}...

Evaluate:
1. Is the content accurate and well-structured?
2. Does it match the target audience level?
3. Are there any gaps or areas needing improvement?
4. Is the tone appropriate?

Respond with JSON:
{{
    "quality_score": 1-10,
    "needs_revision": true/false,
    "feedback": "Your detailed feedback",
    "suggested_improvements": ["improvement1", "improvement2"]
}}"""

        review = await llm_service.generate_structured(
            prompt=review_prompt,
            system_prompt="You are a senior technical editor reviewing blog content for quality and accuracy.",
        )

        needs_revision = review.get("needs_revision", False)
        quality_score = review.get("quality_score", 8)

        # Only allow one revision to avoid infinite loops
        if state.get("revision_count", 0) >= 1:
            needs_revision = False

        return {
            "review_feedback": review.get("feedback", ""),
            "needs_revision": needs_revision and quality_score < 7,
            "revision_count": state.get("revision_count", 0) + 1,
            "current_step": "review_complete",
            "messages": [f"Review complete: Score {quality_score}/10, Needs revision: {needs_revision}"],
            "status": "in_progress",
        }
    except Exception as e:
        return {
            "review_feedback": "",
            "needs_revision": False,
            "current_step": "review_complete",
            "messages": [f"Review skipped due to error: {str(e)}"],
            "status": "in_progress",
        }


async def optimize_node(state: BlogState) -> dict:
    """Optimize node - SEO optimization and final polish."""
    try:
        content_service = get_content_service()

        draft = state.get("draft", {})
        content = draft.get("content", "")

        seo_result = await content_service.optimize_seo(
            content=content,
            keywords=None,
            target_audience=state.get("target_audience"),
        )

        return {
            "final_content": {
                "id": draft.get("id", ""),
                "title": draft.get("title", state["topic"]),
                "content": seo_result.get("optimized_content", content),
                "word_count": draft.get("word_count", 0),
            },
            "seo_metadata": {
                "keywords": seo_result.get("keywords", []),
                "meta_description": seo_result.get("meta_description", ""),
                "suggestions": seo_result.get("suggestions", []),
            },
            "current_step": "complete",
            "messages": ["SEO optimization complete"],
            "status": "completed",
        }
    except Exception as e:
        # If SEO fails, still return the draft as final
        draft = state.get("draft", {})
        return {
            "final_content": draft,
            "seo_metadata": {},
            "current_step": "complete",
            "messages": [f"SEO skipped: {str(e)}, using draft as final"],
            "status": "completed",
        }


def should_revise(state: BlogState) -> str:
    """Conditional edge: determine if revision is needed."""
    if state.get("error"):
        return "end"
    if state.get("needs_revision", False):
        return "draft"
    return "optimize"


def check_error(state: BlogState) -> str:
    """Check if there's an error and should stop."""
    if state.get("error"):
        return "end"
    return "continue"


def create_blog_workflow() -> StateGraph:
    """Create and compile the blog creation workflow."""

    # Create the graph
    workflow = StateGraph(BlogState)

    # Add nodes
    workflow.add_node("research", research_node)
    workflow.add_node("outline", outline_node)
    workflow.add_node("draft", draft_node)
    workflow.add_node("review", review_node)
    workflow.add_node("optimize", optimize_node)

    # Set entry point
    workflow.set_entry_point("research")

    # Add edges
    workflow.add_edge("research", "outline")
    workflow.add_edge("outline", "draft")
    workflow.add_edge("draft", "review")

    # Conditional edge after review
    workflow.add_conditional_edges(
        "review",
        should_revise,
        {
            "draft": "draft",
            "optimize": "optimize",
            "end": END,
        }
    )

    workflow.add_edge("optimize", END)

    return workflow


# Compile the workflow
blog_workflow = create_blog_workflow().compile()


async def save_workflow_results(
    topic: str,
    final_state: dict,
    niche: Optional[str] = None,
    target_audience: str = "intermediate",
) -> dict:
    """Save workflow results to PostgreSQL."""
    saved_ids = {}

    # Save research session
    if final_state.get("research_findings"):
        try:
            research_result = await ResearchSessionRepository.create(
                topic=topic,
                findings=final_state["research_findings"],
                sources=final_state["research_findings"].get("sources", []),
            )
            saved_ids["research_session_id"] = str(research_result.get("id", ""))
        except Exception as e:
            print(f"Failed to save research session: {e}")

    # Save blog post
    if final_state.get("final_content") or final_state.get("draft"):
        content_data = final_state.get("final_content") or final_state.get("draft") or {}
        try:
            blog_result = await BlogPostRepository.create(
                title=content_data.get("title", topic),
                content=content_data.get("content", ""),
                outline=final_state.get("outline"),
                niche=niche,
                target_audience=target_audience,
                word_count=content_data.get("word_count"),
                seo_metadata=final_state.get("seo_metadata"),
                status="completed" if final_state.get("status") == "completed" else "draft",
            )
            saved_ids["blog_post_id"] = str(blog_result.get("id", ""))
            saved_ids["slug"] = blog_result.get("slug", "")
        except Exception as e:
            print(f"Failed to save blog post: {e}")

    return saved_ids


async def run_blog_workflow(
    topic: str,
    niche: Optional[str] = None,
    target_audience: str = "intermediate",
    word_count: int = 2000,
    tone: str = "conversational",
    include_code_examples: bool = True,
    save_to_db: bool = True,
) -> dict:
    """Run the complete blog creation workflow."""

    initial_state: BlogState = {
        "topic": topic,
        "niche": niche,
        "target_audience": target_audience,
        "word_count": word_count,
        "tone": tone,
        "include_code_examples": include_code_examples,
        "current_step": "starting",
        "messages": [f"Starting blog workflow for: {topic}"],
        "research_findings": None,
        "outline": None,
        "draft": None,
        "review_feedback": None,
        "needs_revision": False,
        "revision_count": 0,
        "final_content": None,
        "seo_metadata": None,
        "status": "in_progress",
        "error": None,
    }

    # Run the workflow
    final_state = await blog_workflow.ainvoke(initial_state)

    result = {
        "status": final_state.get("status", "unknown"),
        "topic": topic,
        "messages": final_state.get("messages", []),
        "research": final_state.get("research_findings"),
        "outline": final_state.get("outline"),
        "draft": final_state.get("draft"),
        "final_content": final_state.get("final_content"),
        "seo_metadata": final_state.get("seo_metadata"),
        "error": final_state.get("error"),
    }

    # Save to PostgreSQL if enabled
    if save_to_db and final_state.get("status") == "completed":
        saved_ids = await save_workflow_results(
            topic=topic,
            final_state=final_state,
            niche=niche,
            target_audience=target_audience,
        )
        result["saved"] = saved_ids

    return result
