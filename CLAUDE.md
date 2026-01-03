# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Tech Blog AI is an AI-powered technical content assistant that helps developers create blog posts about Salesforce/Apex, Full-Stack Development (Next.js, TypeScript, PostgreSQL, AWS), and AI/LLM technologies. It uses LangChain, RAG (Retrieval Augmented Generation), and LangGraph for intelligent content generation.

## Tech Stack

- **Language**: Python 3.11+
- **Framework**: FastAPI (async REST API)
- **Package Manager**: UV (fast Python package manager)
- **LLM Provider**: Google Gemini Pro
- **AI Framework**: LangChain + LangGraph
- **Vector Database**: ChromaDB (local semantic search)
- **Database**: PostgreSQL 16
- **Cache**: Redis 7
- **Containerization**: Docker + Docker Compose

## Development Commands

### Using Makefile (Recommended)

```bash
make install     # Create venv and install dependencies
make dev         # Install with dev dependencies
make test        # Run all tests
make test-cov    # Run tests with coverage report
make lint        # Run linters (ruff, mypy)
make format      # Format code (black, ruff)
make run         # Run the app locally
make docker-up   # Start Docker services
make docker-down # Stop Docker services
make clean       # Clean up generated files
```

### Manual Commands

```bash
# Create virtual environment and install dependencies
uv venv
uv pip install -r requirements.txt

# Activate virtual environment
source .venv/bin/activate

# Run the FastAPI app locally
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run tests
pytest tests/ -v

# Run tests with coverage
pytest tests/ --cov=app --cov-report=term-missing

# Run a single test file
pytest tests/test_api/test_health.py -v

# Format and lint
black app/ tests/
ruff check app/ tests/
mypy app/
```

### Docker Commands

```bash
docker-compose up -d      # Start all services
docker-compose ps         # Check container status
docker-compose logs -f app # View application logs
docker-compose down       # Stop all services
```

**API Documentation**: http://localhost:8000/docs (when running)

## Architecture

The application follows a layered architecture:

```
CLIENT LAYER (Web UI, CLI, API Client)
    ↓
API LAYER (FastAPI routes: research, outline, draft, seo)
    ↓
SERVICE LAYER (llm_service, rag_service, content_service)
    ↓
AGENT LAYER (LangGraph blog creation agent: Research → Outline → Draft → Review → Optimize)
    ↓
DATA LAYER (PostgreSQL, ChromaDB vectors, Redis cache, File storage)
```

## Project Structure

```
app/
├── main.py              # FastAPI entry point
├── config.py            # Configuration management
├── api/                 # API Routes
│   ├── research.py      # Topic research endpoints
│   ├── outline.py       # Outline generation
│   ├── explain.py       # Concept explanation
│   ├── draft.py         # Draft writing
│   └── seo.py           # SEO optimization
├── services/            # Business Logic
│   ├── llm_service.py   # Gemini integration
│   ├── rag_service.py   # RAG pipeline
│   ├── research_service.py
│   └── content_service.py
├── agents/              # LangGraph Agents
│   └── blog_agent.py    # Multi-step blog workflow
├── mcp/                 # MCP Tool Integrations
│   ├── file_tools.py    # File system access
│   ├── web_tools.py     # Web search
│   └── db_tools.py      # Database queries
├── models/              # Pydantic Models
│   ├── requests.py
│   └── responses.py
└── db/                  # Database Layer
    ├── postgres.py
    ├── redis.py
    └── chroma.py

modules/                 # Learning modules (01-08)
data/
├── knowledge_base/      # Documents for RAG
└── exports/             # Generated content
tests/
├── test_api/
├── test_services/
└── test_agents/
```

## Key API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/v1/research` | Research a topic |
| POST | `/api/v1/outline` | Generate blog outline |
| POST | `/api/v1/explain` | Explain technical concept |
| POST | `/api/v1/draft` | Generate full blog draft |
| POST | `/api/v1/seo/optimize` | Optimize content for SEO |
| POST | `/api/v1/knowledge/upload` | Add document to knowledge base |
| POST | `/api/v1/knowledge/search` | Semantic search in knowledge base |

## Database Schema

**PostgreSQL tables**: `users`, `blog_posts`, `research_sessions`, `knowledge_documents`

**ChromaDB collections**:
- `tech_blog_knowledge` - General tech documentation
- `salesforce_docs` - Salesforce/Apex references
- `user_content` - User uploaded documents

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| GEMINI_API_KEY | Yes | Google AI API key |
| DATABASE_URL | Yes | PostgreSQL connection string |
| REDIS_URL | No | Redis connection |
| CHROMA_URL | No | ChromaDB server URL |
| DEBUG | No | Enable debug mode |

## AI/LLM Concepts Used

- **LangChain**: Chains, prompts, output parsers in services layer
- **LangGraph**: Stateful multi-step workflows in blog_agent.py
- **RAG**: Knowledge base retrieval + generation in rag_service.py
- **MCP Protocol**: External tool integration in mcp/ directory
- **Embeddings**: Gemini embeddings for semantic similarity search
