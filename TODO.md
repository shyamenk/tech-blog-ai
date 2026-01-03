# TODO.md

Tech Blog AI - Development Task List

---

## Phase 1: Foundation

### 1.1 Project Setup
- [ ] Initialize Python project with `pyproject.toml`
- [ ] Create `requirements.txt` with core dependencies
  - [ ] fastapi, uvicorn
  - [ ] langchain, langchain-google-genai
  - [ ] langgraph
  - [ ] chromadb
  - [ ] psycopg2-binary, asyncpg
  - [ ] redis
  - [ ] pydantic, pydantic-settings
  - [ ] python-dotenv
- [ ] Create `.env.example` with all environment variables
- [ ] Create `.gitignore` for Python/Docker projects

### 1.2 Docker Environment
- [ ] Create `Dockerfile` for FastAPI application
  - [ ] Base image: python:3.11-slim
  - [ ] Install UV package manager
  - [ ] Configure working directory and dependencies
- [ ] Create `docker-compose.yml`
  - [ ] App service (FastAPI on port 8000)
  - [ ] PostgreSQL 16 service (port 5432)
  - [ ] Redis 7 service (port 6379)
  - [ ] ChromaDB service (port 8001)
  - [ ] Define volumes for data persistence
- [ ] Test all containers start correctly with `docker-compose up -d`

### 1.3 Database Initialization
- [ ] Create `init.sql` with PostgreSQL schema
  - [ ] `users` table (id, email, name, api_key_hash, timestamps)
  - [ ] `blog_posts` table (id, user_id, title, slug, content, outline, status, niche, seo_metadata, timestamps)
  - [ ] `research_sessions` table (id, user_id, topic, findings, sources, timestamps)
  - [ ] `knowledge_documents` table (id, user_id, title, content, source_url, embedding_id, metadata, timestamps)
- [ ] Add foreign key constraints and indexes
- [ ] Verify migrations run on container startup

### 1.4 FastAPI Application Skeleton
- [ ] Create directory structure under `app/`
  - [ ] `api/`, `services/`, `agents/`, `mcp/`, `models/`, `db/`
- [ ] Create `app/main.py` with FastAPI app initialization
- [ ] Create `app/config.py` with Pydantic Settings
  - [ ] Load environment variables
  - [ ] Configure database URLs, API keys
- [ ] Add health check endpoint (`GET /health`)
- [ ] Add API versioning (`/api/v1/`)
- [ ] Configure CORS middleware
- [ ] Verify app starts and health check works

### 1.5 Database Connections
- [ ] Create `app/db/postgres.py`
  - [ ] Async connection pool with asyncpg
  - [ ] Connection lifecycle management
- [ ] Create `app/db/redis.py`
  - [ ] Redis client initialization
  - [ ] Connection helper functions
- [ ] Create `app/db/chroma.py`
  - [ ] ChromaDB client connection
  - [ ] Collection initialization helpers

### 1.6 Gemini API Integration
- [ ] Create `app/services/llm_service.py`
  - [ ] Initialize LangChain ChatGoogleGenerativeAI
  - [ ] Create base completion function
  - [ ] Add error handling and retries
  - [ ] Implement token counting utilities
- [ ] Test basic prompt completion works

### 1.7 Basic Prompt Templates
- [ ] Create prompt templates directory `app/prompts/`
- [ ] Create outline generation prompt template
- [ ] Create concept explanation prompt template
- [ ] Create draft writing prompt template
- [ ] Create SEO optimization prompt template

---

## Phase 2: Core Features

### 2.1 Pydantic Models
- [ ] Create `app/models/requests.py`
  - [ ] `ResearchRequest` (topic, niche, depth)
  - [ ] `OutlineRequest` (topic, niche, target_audience, word_count, include_code_examples)
  - [ ] `ExplainRequest` (concept, mode, include_examples)
  - [ ] `DraftRequest` (outline_id, tone, word_count)
  - [ ] `SEOOptimizeRequest` (content, keywords)
  - [ ] `KnowledgeUploadRequest` (title, content, source_url, document_type)
- [ ] Create `app/models/responses.py`
  - [ ] `OutlineResponse` (id, title, hook, sections, estimated_words, seo_suggestions)
  - [ ] `DraftResponse` (id, title, content, word_count, metadata)
  - [ ] `ResearchResponse` (id, topic, findings, sources)
  - [ ] `SEOResponse` (optimized_content, keywords, meta_description, suggestions)

### 2.2 Outline Generation
- [ ] Create `app/api/outline.py` router
  - [ ] `POST /api/v1/outline` endpoint
  - [ ] Request validation
  - [ ] Response formatting
- [ ] Create `app/services/content_service.py`
  - [ ] `generate_outline()` function
  - [ ] Title generation with SEO optimization
  - [ ] Section organization logic
  - [ ] Key points extraction
- [ ] Add outline storage to PostgreSQL

### 2.3 Concept Explainer
- [ ] Create `app/api/explain.py` router
  - [ ] `POST /api/v1/explain` endpoint
- [ ] Add explanation modes to content_service.py
  - [ ] ELI5 mode (simple explanations)
  - [ ] Technical deep-dive mode
  - [ ] Code examples generation
  - [ ] Analogy suggestions

### 2.4 Draft Writer
- [ ] Create `app/api/draft.py` router
  - [ ] `POST /api/v1/draft` endpoint
  - [ ] Link to existing outline by ID
- [ ] Add draft generation to content_service.py
  - [ ] Tone customization (conversational, formal, tutorial)
  - [ ] Code block insertion with language hints
  - [ ] Section transitions
  - [ ] Word count targeting
  - [ ] Markdown output formatting
- [ ] Store generated drafts in `blog_posts` table

### 2.5 ChromaDB Knowledge Base Setup
- [ ] Initialize ChromaDB collections in `app/db/chroma.py`
  - [ ] `tech_blog_knowledge` collection
  - [ ] `salesforce_docs` collection
  - [ ] `user_content` collection
- [ ] Create embedding function using Gemini embeddings
- [ ] Add document chunking utilities

### 2.6 Basic RAG Pipeline
- [ ] Create `app/services/rag_service.py`
  - [ ] Document embedding function
  - [ ] Similarity search function
  - [ ] Context retrieval with relevance scoring
  - [ ] Source citation formatting
- [ ] Create `app/api/knowledge.py` router
  - [ ] `POST /api/v1/knowledge/upload` - Add document
  - [ ] `POST /api/v1/knowledge/search` - Semantic search
  - [ ] `DELETE /api/v1/knowledge/{id}` - Remove document
- [ ] Integrate RAG context into content generation

---

## Phase 3: Advanced Features

### 3.1 LangGraph Blog Creation Agent
- [ ] Create `app/agents/blog_agent.py`
  - [ ] Define agent state schema
  - [ ] Create research node
  - [ ] Create outline node
  - [ ] Create draft node
  - [ ] Create review node
  - [ ] Create optimize node
- [ ] Define state transitions and conditional edges
- [ ] Implement workflow compilation
- [ ] Add streaming support for long-running generations
- [ ] Create endpoint to trigger full blog workflow

### 3.2 Research Service
- [ ] Create `app/services/research_service.py`
  - [ ] Web search integration (via MCP or direct API)
  - [ ] Knowledge base search integration
  - [ ] Source aggregation and deduplication
  - [ ] Confidence scoring for findings
- [ ] Create `app/api/research.py` router
  - [ ] `POST /api/v1/research` endpoint
  - [ ] `GET /api/v1/research/{id}` endpoint
- [ ] Store research sessions in PostgreSQL

### 3.3 MCP Tool Integrations
- [ ] Create `app/mcp/file_tools.py`
  - [ ] File read/write operations
  - [ ] Directory listing
  - [ ] File search
- [ ] Create `app/mcp/web_tools.py`
  - [ ] Web page fetching
  - [ ] Web search queries
  - [ ] URL content extraction
- [ ] Create `app/mcp/db_tools.py`
  - [ ] Database query execution
  - [ ] Schema introspection
- [ ] Register tools with LangChain/LangGraph agents

### 3.4 SEO Optimization
- [ ] Create `app/api/seo.py` router
  - [ ] `POST /api/v1/seo/optimize` endpoint
- [ ] Add SEO analysis to content_service.py
  - [ ] Keyword density analysis
  - [ ] Meta description generation
  - [ ] Title tag optimization
  - [ ] Header structure validation (H1, H2, H3)
  - [ ] Internal linking suggestions
  - [ ] Readability scoring

### 3.5 Redis Caching Layer
- [ ] Implement caching in `app/db/redis.py`
  - [ ] Cache decorator for service functions
  - [ ] TTL configuration per cache type
- [ ] Add caching to expensive operations
  - [ ] LLM completions (by prompt hash)
  - [ ] Research results
  - [ ] Embedding lookups
- [ ] Implement cache invalidation strategies

### 3.6 Rate Limiting
- [ ] Add rate limiting middleware
  - [ ] Per-user rate limits
  - [ ] Per-endpoint rate limits
- [ ] Store rate limit counters in Redis
- [ ] Return appropriate 429 responses

---

## Phase 4: Polish & Documentation

### 4.1 Test Suite
- [ ] Set up pytest with async support
- [ ] Create `tests/conftest.py` with fixtures
  - [ ] Test database setup/teardown
  - [ ] Mock LLM responses
  - [ ] Test client fixture
- [ ] Create `tests/test_api/`
  - [ ] Test outline endpoints
  - [ ] Test explain endpoints
  - [ ] Test draft endpoints
  - [ ] Test SEO endpoints
  - [ ] Test knowledge base endpoints
  - [ ] Test research endpoints
- [ ] Create `tests/test_services/`
  - [ ] Test llm_service
  - [ ] Test rag_service
  - [ ] Test content_service
  - [ ] Test research_service
- [ ] Create `tests/test_agents/`
  - [ ] Test blog_agent workflow
  - [ ] Test individual agent nodes

### 4.2 API Documentation
- [ ] Add OpenAPI metadata to all endpoints
  - [ ] Descriptions
  - [ ] Request/response examples
  - [ ] Error responses
- [ ] Configure Swagger UI at `/docs`
- [ ] Configure ReDoc at `/redoc`
- [ ] Add API usage examples to README

### 4.3 Learning Modules
- [ ] Create `modules/` directory structure
- [ ] `01_ai_fundamentals/` - Tokens, context, embeddings basics
- [ ] `02_langchain_basics/` - Chains, prompts, output parsers
- [ ] `03_prompt_engineering/` - Zero-shot, few-shot, CoT techniques
- [ ] `04_vector_databases/` - Embeddings, similarity search
- [ ] `05_rag/` - Retrieval augmented generation pipeline
- [ ] `06_langgraph/` - Stateful workflows, agents
- [ ] `07_mcp/` - Model Context Protocol, tool integration
- [ ] `08_integration/` - Putting it all together

### 4.4 Data Directories
- [ ] Create `data/knowledge_base/` for RAG documents
- [ ] Create `data/exports/` for generated content
- [ ] Add sample documents to knowledge base
  - [ ] Salesforce/Apex reference docs
  - [ ] Next.js documentation excerpts
  - [ ] AI/LLM concept explanations

### 4.5 Performance Optimization
- [ ] Profile slow endpoints
- [ ] Optimize database queries
  - [ ] Add missing indexes
  - [ ] Use connection pooling effectively
- [ ] Implement async operations where blocking
- [ ] Add request/response compression

### 4.6 Final Documentation
- [ ] Update README.md with complete setup instructions
- [ ] Document all environment variables
- [ ] Add architecture diagrams
- [ ] Create contribution guidelines
- [ ] Add troubleshooting guide

---

## Quick Reference

### Priority Order
1. Phase 1 must be complete before Phase 2
2. Within phases, complete numbered sections in order
3. Database and service layers before API layers
4. Tests can be written alongside features

### Key Dependencies
- Docker environment → All other tasks
- PostgreSQL schema → Database connection code
- LLM service → All content generation features
- ChromaDB setup → RAG pipeline
- RAG pipeline → Research service
- All services → LangGraph agent

### Definition of Done
- [ ] Code compiles without errors
- [ ] Endpoint returns expected response
- [ ] Basic error handling in place
- [ ] Tested manually via `/docs`
