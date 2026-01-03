# Tech Blog AI

AI-Powered Technical Content Assistant for developers creating high-quality blog posts about Salesforce/Apex, Full-Stack Development, and AI/LLM technologies.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![LangChain](https://img.shields.io/badge/LangChain-Latest-orange.svg)](https://python.langchain.com)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue.svg)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [API Reference](#api-reference)
- [Database Schema](#database-schema)
- [AI/LLM Concepts](#aillm-concepts)
- [Development](#development)
- [License](#license)

---

## Overview

Tech Blog AI leverages modern AI technologies including **LangChain**, **RAG (Retrieval Augmented Generation)**, and **LangGraph** to provide intelligent content generation, topic research, and SEO optimization capabilities.

### Key Objectives

- Reduce time spent on technical blog content creation by 60%
- Provide research-backed, accurate technical content
- Generate SEO-optimized blog posts with proper structure
- Serve as a learning platform for modern AI/LLM development

### Target Users

- Salesforce Developers building authority through content
- Full-stack developers documenting solutions
- AI/ML practitioners sharing knowledge
- Developer advocates and technical writers

---

## Key Features

| Feature | Description |
|---------|-------------|
| **Topic Research** | AI-powered research using web search and knowledge base |
| **Outline Generator** | Creates structured blog outlines with SEO considerations |
| **Concept Explainer** | Explains technical concepts at various complexity levels |
| **Draft Writer** | Generates full blog posts from outlines with tone customization |
| **SEO Optimizer** | Analyzes and optimizes content for search engines |
| **Knowledge Base** | RAG-powered document storage and semantic search |

---

## Architecture

### High-Level System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              CLIENT LAYER                                    │
│  ┌───────────────┐    ┌───────────────┐    ┌───────────────┐               │
│  │    Web UI     │    │   CLI Tool    │    │  API Client   │               │
│  │   (Future)    │    │   (Future)    │    │    (REST)     │               │
│  └───────────────┘    └───────────────┘    └───────────────┘               │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           API LAYER (FastAPI)                                │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │ Research │  │ Outline  │  │  Draft   │  │ Explain  │  │   SEO    │      │
│  │   API    │  │   API    │  │   API    │  │   API    │  │   API    │      │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘      │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                            SERVICE LAYER                                     │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐                 │
│  │  LLM Service   │  │  RAG Service   │  │Content Service │                 │
│  │   (Gemini)     │  │  (ChromaDB)    │  │  (Generation)  │                 │
│  └────────────────┘  └────────────────┘  └────────────────┘                 │
│  ┌────────────────┐                                                          │
│  │Research Service│                                                          │
│  │  (Web + KB)    │                                                          │
│  └────────────────┘                                                          │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         AGENT LAYER (LangGraph)                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                      Blog Creation Agent                             │    │
│  │  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐         │    │
│  │  │ Research │ → │ Outline  │ → │  Draft   │ → │  Review  │ → ...   │    │
│  │  └──────────┘   └──────────┘   └──────────┘   └──────────┘         │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                             DATA LAYER                                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │  PostgreSQL  │  │   ChromaDB   │  │    Redis     │  │    Files     │    │
│  │    (Data)    │  │  (Vectors)   │  │   (Cache)    │  │  (Storage)   │    │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
```

### LangGraph Agent Workflow

```
                              ┌─────────────┐
                              │    START    │
                              └──────┬──────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │   1. RESEARCH TOPIC   │
                         │   - Web search        │
                         │   - Knowledge base    │
                         │   - Source gathering  │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │  2. GENERATE OUTLINE  │
                         │   - Title creation    │
                         │   - Section planning  │
                         │   - SEO keywords      │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │   3. WRITE DRAFT      │
                         │   - Content generation│
                         │   - Code examples     │
                         │   - Markdown format   │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │   4. REVIEW CONTENT   │
                         │   - Quality check     │
                         │   - Accuracy verify   │
                         │   - Flow analysis     │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │   5. SEO OPTIMIZE     │
                         │   - Keyword density   │
                         │   - Meta description  │
                         │   - Header structure  │
                         └───────────┬───────────┘
                                     │
                                     ▼
                              ┌─────────────┐
                              │     END     │
                              └─────────────┘
```

### Docker Container Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Docker Compose Network                        │
│                                                                      │
│  ┌─────────────────┐     ┌─────────────────┐                        │
│  │      app        │     │    postgres     │                        │
│  │  python:3.11    │────▶│  postgres:16    │                        │
│  │   Port: 8000    │     │   Port: 5432    │                        │
│  └────────┬────────┘     └─────────────────┘                        │
│           │                                                          │
│           │              ┌─────────────────┐                        │
│           │              │     redis       │                        │
│           └─────────────▶│   redis:7       │                        │
│           │              │   Port: 6379    │                        │
│           │              └─────────────────┘                        │
│           │                                                          │
│           │              ┌─────────────────┐                        │
│           │              │     chroma      │                        │
│           └─────────────▶│  chromadb       │                        │
│                          │   Port: 8001    │                        │
│                          └─────────────────┘                        │
│                                                                      │
│  Volumes:                                                            │
│  - postgres_data    (PostgreSQL persistence)                        │
│  - redis_data       (Redis persistence)                             │
│  - chroma_data      (Vector embeddings)                             │
│  - ./app            (Application code - hot reload)                 │
│  - ./data           (Knowledge base & exports)                      │
└─────────────────────────────────────────────────────────────────────┘
```

### RAG Pipeline Architecture

```
┌──────────────────────────────────────────────────────────────────────────┐
│                          RAG PIPELINE                                     │
│                                                                           │
│  ┌─────────────┐                                                         │
│  │  Document   │                                                         │
│  │   Upload    │                                                         │
│  └──────┬──────┘                                                         │
│         │                                                                 │
│         ▼                                                                 │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────────────────┐    │
│  │   Chunk     │────▶│   Embed     │────▶│   Store in ChromaDB     │    │
│  │  Document   │     │  (Gemini)   │     │  - tech_blog_knowledge  │    │
│  └─────────────┘     └─────────────┘     │  - salesforce_docs      │    │
│                                          │  - user_content         │    │
│                                          └─────────────────────────┘    │
│                                                       │                  │
│  ┌─────────────┐                                      │                  │
│  │   User      │                                      ▼                  │
│  │   Query     │     ┌─────────────┐     ┌─────────────────────────┐    │
│  └──────┬──────┘     │   Embed     │     │   Similarity Search     │    │
│         │            │   Query     │────▶│   (Top-K retrieval)     │    │
│         └───────────▶│  (Gemini)   │     └───────────┬─────────────┘    │
│                      └─────────────┘                 │                  │
│                                                      ▼                  │
│                                          ┌─────────────────────────┐    │
│                                          │   Retrieved Context     │    │
│                                          │   + Source Citations    │    │
│                                          └───────────┬─────────────┘    │
│                                                      │                  │
│                                                      ▼                  │
│                                          ┌─────────────────────────┐    │
│                                          │   LLM Generation        │    │
│                                          │   (Context + Query)     │    │
│                                          └───────────┬─────────────┘    │
│                                                      │                  │
│                                                      ▼                  │
│                                          ┌─────────────────────────┐    │
│                                          │   Final Response        │    │
│                                          └─────────────────────────┘    │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## Tech Stack

### Core Technologies

| Component | Technology | Purpose |
|-----------|------------|---------|
| Language | Python 3.11+ | Primary development language |
| Framework | FastAPI | Async REST API framework |
| Package Manager | UV | Fast Python package management |
| LLM Provider | Google Gemini Pro | Free tier AI model |
| AI Framework | LangChain + LangGraph | LLM orchestration & agents |
| Vector Database | ChromaDB | Local semantic search |
| Database | PostgreSQL 16 | Persistent data storage |
| Cache | Redis 7 | Caching & rate limiting |
| Containerization | Docker + Docker Compose | Development & deployment |

### AI/LLM Stack

| Technology | Description |
|------------|-------------|
| LangChain | Framework for building LLM applications - chains, prompts, output parsers |
| LangGraph | Multi-step AI workflows with state management for complex agent behaviors |
| ChromaDB | Local vector database for document embeddings and semantic search (RAG) |
| MCP Protocol | Model Context Protocol for external tool integration |
| Gemini Embeddings | Text embeddings for semantic similarity and document retrieval |

---

## Project Structure

```
tech-blog-ai/
├── docker-compose.yml          # Container orchestration
├── Dockerfile                  # App container definition
├── pyproject.toml              # UV/Python project config
├── requirements.txt            # Dependencies
├── .env.example                # Environment template
├── init.sql                    # Database initialization
│
├── app/                        # Main Application
│   ├── __init__.py
│   ├── main.py                 # FastAPI entry point
│   ├── config.py               # Configuration management
│   │
│   ├── api/                    # API Routes
│   │   ├── __init__.py
│   │   ├── research.py         # Topic research endpoints
│   │   ├── outline.py          # Outline generation
│   │   ├── explain.py          # Concept explanation
│   │   ├── draft.py            # Draft writing
│   │   └── seo.py              # SEO optimization
│   │
│   ├── services/               # Business Logic
│   │   ├── __init__.py
│   │   ├── llm_service.py      # Gemini integration
│   │   ├── rag_service.py      # RAG pipeline
│   │   ├── research_service.py # Web research
│   │   └── content_service.py  # Content generation
│   │
│   ├── agents/                 # LangGraph Agents
│   │   ├── __init__.py
│   │   └── blog_agent.py       # Multi-step blog workflow
│   │
│   ├── mcp/                    # MCP Tool Integrations
│   │   ├── __init__.py
│   │   ├── file_tools.py       # File system access
│   │   ├── web_tools.py        # Web search
│   │   └── db_tools.py         # Database queries
│   │
│   ├── models/                 # Pydantic Models
│   │   ├── __init__.py
│   │   ├── requests.py         # Request schemas
│   │   └── responses.py        # Response schemas
│   │
│   └── db/                     # Database Layer
│       ├── __init__.py
│       ├── postgres.py         # PostgreSQL connection
│       ├── redis.py            # Redis connection
│       └── chroma.py           # ChromaDB connection
│
├── modules/                    # Learning Modules
│   ├── 01_ai_fundamentals/
│   ├── 02_langchain_basics/
│   ├── 03_prompt_engineering/
│   ├── 04_vector_databases/
│   ├── 05_rag/
│   ├── 06_langgraph/
│   ├── 07_mcp/
│   └── 08_integration/
│
├── data/                       # Data Storage
│   ├── knowledge_base/         # Documents for RAG
│   └── exports/                # Generated content
│
└── tests/                      # Test Suite
    ├── __init__.py
    ├── conftest.py
    ├── test_api/
    ├── test_services/
    └── test_agents/
```

---

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Git
- Google AI API Key ([Get one here](https://aistudio.google.com/apikey))

### Quick Start

```bash
# Clone the repository
git clone https://github.com/shyamenk/tech-blog-ai.git
cd tech-blog-ai

# Create environment file
cp .env.example .env

# Add your GEMINI_API_KEY to .env
nano .env  # or use your preferred editor

# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f app

# Access API documentation
# Open http://localhost:8000/docs in your browser
```

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GEMINI_API_KEY` | Yes | Google AI API key |
| `DATABASE_URL` | Yes | PostgreSQL connection string |
| `REDIS_URL` | No | Redis connection |
| `CHROMA_URL` | No | ChromaDB server URL |
| `DEBUG` | No | Enable debug mode |

### Stopping Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (clears all data)
docker-compose down -v
```

---

## API Reference

### Base URL

```
http://localhost:8000/api/v1
```

### Endpoints

#### Research API

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/research` | Research a topic and return findings |
| `GET` | `/research/{id}` | Get research session by ID |

#### Content Generation API

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/outline` | Generate blog post outline |
| `POST` | `/explain` | Explain a technical concept |
| `POST` | `/draft` | Generate full blog draft |
| `POST` | `/seo/optimize` | Optimize content for SEO |

#### Knowledge Base API

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/knowledge/upload` | Upload document to knowledge base |
| `POST` | `/knowledge/search` | Semantic search in knowledge base |
| `DELETE` | `/knowledge/{id}` | Remove document from knowledge base |

### Example Request

**POST /api/v1/outline**

```json
{
  "topic": "Building REST APIs with Apex",
  "niche": "salesforce",
  "target_audience": "intermediate",
  "word_count": 2000,
  "include_code_examples": true
}
```

**Response**

```json
{
  "id": "outline_abc123",
  "title": "Building REST APIs with Apex: A Complete Guide",
  "hook": "Learn how to expose Salesforce data...",
  "sections": [
    {
      "title": "Introduction to Apex REST",
      "points": ["..."]
    },
    {
      "title": "Setting Up Your First Endpoint",
      "points": ["..."]
    }
  ],
  "estimated_words": 2100,
  "seo_suggestions": {
    "keywords": ["apex rest api", "salesforce api"],
    "meta_description": "..."
  }
}
```

---

## Database Schema

### PostgreSQL Tables

#### users
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    api_key_hash VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### blog_posts
```sql
CREATE TABLE blog_posts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    title VARCHAR(500) NOT NULL,
    slug VARCHAR(500) UNIQUE,
    content TEXT,
    outline JSONB,
    status VARCHAR(50) DEFAULT 'draft',
    niche VARCHAR(100),
    target_audience VARCHAR(100),
    word_count INTEGER,
    seo_metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### research_sessions
```sql
CREATE TABLE research_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    topic VARCHAR(500) NOT NULL,
    findings JSONB,
    sources JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### knowledge_documents
```sql
CREATE TABLE knowledge_documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    title VARCHAR(500),
    content TEXT,
    source_url VARCHAR(1000),
    document_type VARCHAR(50),
    embedding_id VARCHAR(255),
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### ChromaDB Collections

| Collection | Purpose | Metadata |
|------------|---------|----------|
| `tech_blog_knowledge` | General tech documentation | source, niche, doc_type |
| `salesforce_docs` | Salesforce/Apex references | api_version, doc_type |
| `user_content` | User uploaded documents | user_id, upload_date |

---

## AI/LLM Concepts

This project demonstrates key AI/LLM concepts:

| Concept | Where Applied | Learning Outcome |
|---------|---------------|------------------|
| LLM Fundamentals | Throughout - Gemini integration | Tokens, context windows, embeddings |
| LangChain | Services layer | Chains, prompts, output parsers |
| Prompt Engineering | Content generation | Zero-shot, few-shot, Chain of Thought |
| Vector Databases | Knowledge base (ChromaDB) | Embeddings, similarity search |
| RAG | Research & context injection | Retrieval + generation pipeline |
| LangGraph | Blog creation agent | Stateful workflows, agents |
| MCP | External tool integration | Tool calling, function execution |

---

## Development

### Running Locally (without Docker)

```bash
# Install UV package manager
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment
uv venv
source .venv/bin/activate

# Install dependencies
uv pip install -r requirements.txt

# Run the application
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_api/test_outline.py
```

### Code Quality

```bash
# Format code
black app/

# Lint code
ruff check app/

# Type checking
mypy app/
```

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Useful Links

- [Gemini API](https://aistudio.google.com/apikey)
- [LangChain Docs](https://python.langchain.com/docs/)
- [LangGraph Docs](https://langchain-ai.github.io/langgraph/)
- [ChromaDB Docs](https://docs.trychroma.com/)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [UV Package Manager](https://github.com/astral-sh/uv)
