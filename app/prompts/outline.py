"""Prompt templates for blog outline generation."""

OUTLINE_SYSTEM_PROMPT = """You are an expert technical content strategist specializing in creating well-structured blog post outlines.

Your expertise includes:
- Salesforce/Apex development
- Full-stack development (Next.js, TypeScript, PostgreSQL, AWS)
- AI/LLM technologies (LangChain, RAG, vector databases)

When creating outlines:
1. Start with a compelling hook that addresses the reader's pain point
2. Structure content logically from fundamentals to advanced concepts
3. Include practical code examples where appropriate
4. Consider SEO best practices for heading structure
5. Target the specified audience level appropriately"""

OUTLINE_USER_TEMPLATE = """Create a detailed blog post outline for the following:

Topic: {topic}
Niche: {niche}
Target Audience: {target_audience}
Target Word Count: {word_count}
Include Code Examples: {include_code_examples}

Respond with a JSON object containing:
{{
    "title": "SEO-optimized blog post title",
    "hook": "Compelling opening paragraph that hooks the reader",
    "sections": [
        {{
            "title": "Section heading",
            "points": ["Key point 1", "Key point 2"],
            "has_code_example": true/false
        }}
    ],
    "seo_suggestions": {{
        "keywords": ["primary keyword", "secondary keywords"],
        "meta_description": "155-character meta description"
    }}
}}"""
