"""Content generation service using LLM."""

import uuid
import json
from typing import Optional, Any

from app.services.llm_service import LLMService, get_llm_service
from app.prompts.outline import OUTLINE_SYSTEM_PROMPT, OUTLINE_USER_TEMPLATE
from app.prompts.explain import EXPLAIN_SYSTEM_PROMPT, EXPLAIN_USER_TEMPLATE
from app.prompts.draft import DRAFT_SYSTEM_PROMPT, DRAFT_USER_TEMPLATE
from app.prompts.seo import SEO_SYSTEM_PROMPT, SEO_USER_TEMPLATE


class ContentService:
    """Service for generating blog content using LLM."""

    def __init__(self, llm_service: Optional[LLMService] = None):
        self.llm = llm_service or get_llm_service()

    async def generate_outline(
        self,
        topic: str,
        niche: Optional[str] = None,
        target_audience: str = "intermediate",
        word_count: int = 2000,
        include_code_examples: bool = True,
    ) -> dict[str, Any]:
        """Generate a blog post outline."""
        prompt = OUTLINE_USER_TEMPLATE.format(
            topic=topic,
            niche=niche or "general tech",
            target_audience=target_audience,
            word_count=word_count,
            include_code_examples=include_code_examples,
        )

        response = await self.llm.generate_structured(
            prompt=prompt,
            system_prompt=OUTLINE_SYSTEM_PROMPT,
        )

        # Add ID if not present
        if "id" not in response:
            response["id"] = f"outline_{uuid.uuid4().hex[:12]}"

        # Ensure required fields exist
        response.setdefault("title", f"Guide to {topic}")
        response.setdefault("hook", "")
        response.setdefault("sections", [])
        response.setdefault("seo_suggestions", {})

        # Calculate estimated words if not present
        if "estimated_words" not in response:
            response["estimated_words"] = word_count

        return response

    async def explain_concept(
        self,
        concept: str,
        mode: str = "technical",
        include_examples: bool = True,
        include_analogies: bool = True,
    ) -> dict[str, Any]:
        """Explain a technical concept."""
        prompt = EXPLAIN_USER_TEMPLATE.format(
            concept=concept,
            mode=mode,
            include_examples=include_examples,
            include_analogies=include_analogies,
        )

        response = await self.llm.generate_structured(
            prompt=prompt,
            system_prompt=EXPLAIN_SYSTEM_PROMPT,
        )

        # Ensure required fields exist
        response.setdefault("concept", concept)
        response.setdefault("explanation", "")
        response.setdefault("examples", [])
        response.setdefault("analogies", [])
        response.setdefault("mode", mode)

        return response

    async def generate_draft(
        self,
        topic: str,
        outline: Optional[dict] = None,
        tone: str = "conversational",
        word_count: int = 2000,
        include_code_examples: bool = True,
    ) -> dict[str, Any]:
        """Generate a full blog post draft."""
        outline_str = json.dumps(outline, indent=2) if outline else "No outline provided"

        prompt = DRAFT_USER_TEMPLATE.format(
            topic=topic,
            outline=outline_str,
            tone=tone,
            word_count=word_count,
            include_code_examples=include_code_examples,
        )

        # For draft, we want markdown output, not JSON
        content = await self.llm.generate(
            prompt=prompt,
            system_prompt=DRAFT_SYSTEM_PROMPT,
        )

        # Extract title from content if possible
        title = topic
        if content.startswith("# "):
            first_line = content.split("\n")[0]
            title = first_line.replace("# ", "").strip()

        # Count actual words
        actual_word_count = len(content.split())

        return {
            "id": f"draft_{uuid.uuid4().hex[:12]}",
            "title": title,
            "content": content,
            "word_count": actual_word_count,
            "metadata": {
                "tone": tone,
                "target_word_count": word_count,
                "has_code_examples": include_code_examples,
            },
        }

    async def optimize_seo(
        self,
        content: str,
        keywords: Optional[list[str]] = None,
        target_audience: Optional[str] = None,
    ) -> dict[str, Any]:
        """Optimize content for SEO."""
        prompt = SEO_USER_TEMPLATE.format(
            content=content[:5000],  # Limit content length
            keywords=", ".join(keywords) if keywords else "auto-detect",
            target_audience=target_audience or "developers",
        )

        response = await self.llm.generate_structured(
            prompt=prompt,
            system_prompt=SEO_SYSTEM_PROMPT,
        )

        # Ensure required fields exist
        response.setdefault("optimized_content", content)
        response.setdefault("keywords", keywords or [])
        response.setdefault("meta_description", "")
        response.setdefault("suggestions", [])

        return response


# Singleton instance
_content_service: Optional[ContentService] = None


def get_content_service() -> ContentService:
    """Get or create content service instance."""
    global _content_service
    if _content_service is None:
        _content_service = ContentService()
    return _content_service
