"""Pytest configuration and fixtures."""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def mock_llm_response():
    """Mock LLM response for testing."""
    return {
        "title": "Test Blog Post",
        "content": "This is test content.",
    }
