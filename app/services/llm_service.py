"""LLM Service for Google Gemini integration."""

from typing import Optional, Any
from functools import lru_cache

from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser

from app.config import get_settings


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

    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
    ) -> str:
        """Generate a response from the LLM."""
        messages = []

        if system_prompt:
            messages.append(SystemMessage(content=system_prompt))

        messages.append(HumanMessage(content=prompt))

        # Override temperature if provided
        model = self.chat_model
        if temperature is not None:
            model = self.chat_model.bind(temperature=temperature)

        response = await model.ainvoke(messages)
        return response.content

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

    async def embed_text(self, text: str) -> list[float]:
        """Generate embeddings for a text."""
        return await self.embeddings.aembed_query(text)

    async def embed_documents(self, documents: list[str]) -> list[list[float]]:
        """Generate embeddings for multiple documents."""
        return await self.embeddings.aembed_documents(documents)

    def count_tokens(self, text: str) -> int:
        """Estimate token count for text."""
        # Rough estimation: ~4 characters per token for English
        return len(text) // 4


@lru_cache
def get_llm_service() -> LLMService:
    """Get cached LLM service instance."""
    return LLMService()
