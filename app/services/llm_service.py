"""LLM Service for Google Gemini integration with Redis caching."""

from typing import Optional, Any
from functools import lru_cache
import hashlib

from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser

from app.config import get_settings
from app.db.redis import cache_get, cache_set, CACHE_TTL_LONG, CACHE_TTL_DAY


class LLMService:
    """Service for interacting with Google Gemini LLM."""

    def __init__(self):
        settings = get_settings()
        self.api_key = settings.gemini_api_key

        # Initialize the chat model
        self.chat_model = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=self.api_key,
            temperature=0.7,
            max_output_tokens=4096,
            convert_system_message_to_human=True,
        )

        # Initialize embeddings model
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=self.api_key,
        )

        # Output parsers
        self.str_parser = StrOutputParser()
        self.json_parser = JsonOutputParser()

    def _generate_cache_key(self, prefix: str, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Generate a cache key for LLM requests."""
        key_data = f"{prompt}:{system_prompt or ''}"
        key_hash = hashlib.md5(key_data.encode()).hexdigest()[:16]
        return f"llm:{prefix}:{key_hash}"

    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        use_cache: bool = True,
    ) -> str:
        """Generate a response from the LLM with optional caching."""
        # Try cache first (only for deterministic requests)
        cache_key = None
        if use_cache and temperature in (None, 0.7):
            cache_key = self._generate_cache_key("gen", prompt, system_prompt)
            try:
                cached = await cache_get(cache_key)
                if cached:
                    return cached
            except Exception:
                pass  # Redis unavailable, continue without cache

        messages = []

        if system_prompt:
            messages.append(SystemMessage(content=system_prompt))

        messages.append(HumanMessage(content=prompt))

        # Override temperature if provided
        model = self.chat_model
        if temperature is not None:
            model = self.chat_model.bind(temperature=temperature)

        response = await model.ainvoke(messages)
        result = response.content

        # Cache the result
        if cache_key:
            try:
                await cache_set(cache_key, result, ttl=CACHE_TTL_LONG)
            except Exception:
                pass  # Redis unavailable, continue without caching

        return result

    async def generate_with_template(
        self,
        template: ChatPromptTemplate,
        variables: dict[str, Any],
        parse_json: bool = False,
    ) -> Any:
        """Generate using a prompt template."""
        chain = template | self.chat_model

        if parse_json:
            chain = chain | self.json_parser
        else:
            chain = chain | self.str_parser

        return await chain.ainvoke(variables)

    async def generate_structured(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
    ) -> dict:
        """Generate a structured JSON response."""
        json_instruction = "\n\nRespond with valid JSON only, no markdown formatting."

        full_prompt = prompt + json_instruction

        response = await self.generate(
            prompt=full_prompt,
            system_prompt=system_prompt,
            temperature=0.3,  # Lower temperature for structured output
        )

        # Parse the response as JSON
        import json
        try:
            # Try to extract JSON from the response
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]
            if response.startswith("```"):
                response = response[3:]
            if response.endswith("```"):
                response = response[:-3]
            return json.loads(response.strip())
        except json.JSONDecodeError:
            return {"raw_response": response}

    async def embed_text(self, text: str, use_cache: bool = True) -> list[float]:
        """Generate embeddings for a text with optional caching."""
        cache_key = None
        if use_cache:
            cache_key = self._generate_cache_key("emb", text)
            try:
                cached = await cache_get(cache_key)
                if cached:
                    return cached
            except Exception:
                pass

        result = await self.embeddings.aembed_query(text)

        if cache_key:
            try:
                await cache_set(cache_key, result, ttl=CACHE_TTL_DAY)
            except Exception:
                pass

        return result

    async def embed_documents(self, documents: list[str], use_cache: bool = True) -> list[list[float]]:
        """Generate embeddings for multiple documents with optional caching."""
        # For documents, we cache each individually
        results = []
        for doc in documents:
            embedding = await self.embed_text(doc, use_cache=use_cache)
            results.append(embedding)
        return results

    def count_tokens(self, text: str) -> int:
        """Estimate token count for text."""
        # Rough estimation: ~4 characters per token for English
        return len(text) // 4


@lru_cache
def get_llm_service() -> LLMService:
    """Get cached LLM service instance."""
    return LLMService()
