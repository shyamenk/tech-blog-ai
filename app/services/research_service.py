"""Research service for topic research using LLM."""

import uuid
from typing import Optional, Any

from app.services.llm_service import LLMService, get_llm_service


RESEARCH_SYSTEM_PROMPT = """You are an expert technical researcher specializing in software development topics.

Your research areas include:
- Salesforce/Apex development
- Full-stack development (Next.js, TypeScript, PostgreSQL, AWS)
- AI/LLM technologies (LangChain, RAG, vector databases)

When researching a topic:
1. Provide comprehensive, accurate findings
2. Include key concepts and best practices
3. Cite common sources and documentation
4. Identify potential challenges and solutions
5. Rate confidence level for each finding"""

RESEARCH_USER_TEMPLATE = """Research the following topic in depth:

Topic: {topic}
Niche: {niche}
Research Depth: {depth}

Respond with a JSON object containing:
{{
    "topic": "The researched topic",
    "summary": "A brief 2-3 sentence summary of the topic",
    "findings": [
        {{
            "title": "Finding title",
            "content": "Detailed explanation of the finding",
            "confidence": 0.95,
            "source": "Documentation or reference"
        }}
    ],
    "key_concepts": ["concept1", "concept2"],
    "best_practices": ["practice1", "practice2"],
    "common_challenges": ["challenge1", "challenge2"],
    "recommended_resources": ["resource1", "resource2"]
}}"""


class ResearchService:
    """Service for researching topics using LLM."""

    def __init__(self, llm_service: Optional[LLMService] = None):
        self.llm = llm_service or get_llm_service()

    async def research_topic(
        self,
        topic: str,
        niche: Optional[str] = None,
        depth: str = "medium",
    ) -> dict[str, Any]:
        """Research a topic and return findings."""
        prompt = RESEARCH_USER_TEMPLATE.format(
            topic=topic,
            niche=niche or "general tech",
            depth=depth,
        )

        response = await self.llm.generate_structured(
            prompt=prompt,
            system_prompt=RESEARCH_SYSTEM_PROMPT,
        )

        # Add ID if not present
        if "id" not in response:
            response["id"] = f"research_{uuid.uuid4().hex[:12]}"

        # Ensure required fields exist
        response.setdefault("topic", topic)
        response.setdefault("findings", [])
        response.setdefault("sources", [])

        # Extract sources from findings if present
        if not response.get("sources") and response.get("findings"):
            sources = []
            for finding in response["findings"]:
                if isinstance(finding, dict) and finding.get("source"):
                    sources.append(finding["source"])
            response["sources"] = sources

        return response


# Singleton instance
_research_service: Optional[ResearchService] = None


def get_research_service() -> ResearchService:
    """Get or create research service instance."""
    global _research_service
    if _research_service is None:
        _research_service = ResearchService()
    return _research_service
