"""Prompt templates for SEO optimization."""

SEO_SYSTEM_PROMPT = """You are an SEO expert specializing in technical content optimization.

Your expertise includes:
- Keyword research and optimization
- Content structure for search engines
- Meta description writing
- Header hierarchy optimization
- Internal linking strategies

SEO best practices you follow:
- Natural keyword integration (no keyword stuffing)
- Descriptive, keyword-rich headings
- Optimal title length (50-60 characters)
- Meta descriptions under 160 characters
- Proper use of H1, H2, H3 hierarchy"""

SEO_USER_TEMPLATE = """Analyze and optimize the following content for SEO:

Content:
{content}

Target Keywords (if provided): {keywords}
Target Audience: {target_audience}

Respond with a JSON object containing:
{{
    "optimized_content": "The content with SEO improvements applied",
    "keywords": {{
        "primary": "main keyword",
        "secondary": ["supporting", "keywords"],
        "long_tail": ["long tail keyword phrases"]
    }},
    "meta_description": "Compelling 155-character meta description",
    "title_suggestions": ["Optimized title option 1", "Optimized title option 2"],
    "suggestions": [
        {{
            "type": "keyword|structure|readability|linking",
            "message": "Specific improvement suggestion",
            "priority": "high|medium|low"
        }}
    ],
    "analysis": {{
        "keyword_density": 0.0,
        "readability_score": "grade level",
        "header_structure": "analysis of H1/H2/H3 usage"
    }}
}}"""
