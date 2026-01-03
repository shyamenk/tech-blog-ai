# TODO.md

Tech Blog AI - Development Task List

---

## Phase 1: Foundation [COMPLETED]

### 1.1 Project Setup
- [x] Initialize Python project with `pyproject.toml`
- [x] Create `requirements.txt` with core dependencies
- [x] Create `.env.example` with all environment variables
- [x] Create `.gitignore` for Python/Docker projects

### 1.2 Docker Environment
- [x] Create `Dockerfile` for FastAPI application
- [x] Create `docker-compose.yml` with all services
- [x] Test all containers configuration

### 1.3 Database Initialization
- [x] Create `init.sql` with PostgreSQL schema (users, blog_posts, research_sessions, knowledge_documents)
- [x] Add foreign key constraints and indexes
- [x] Add auto-update triggers

### 1.4 FastAPI Application Skeleton
- [x] Create directory structure under `app/`
- [x] Create `app/main.py` with FastAPI app initialization
- [x] Create `app/config.py` with Pydantic Settings
- [x] Add health check endpoint, API versioning, CORS middleware
- [x] Create all API route files (research, outline, explain, draft, seo, knowledge)
- [x] Create Pydantic models (requests.py, responses.py)

### 1.5 Database Connections
- [x] Create `app/db/postgres.py` with async pool
- [x] Create `app/db/redis.py` with caching utilities
- [x] Create `app/db/chroma.py` with collection helpers

### 1.6 Gemini API Integration
- [x] Create `app/services/llm_service.py` with LangChain integration
- [x] Implement generate, generate_structured, embed functions

### 1.7 Basic Prompt Templates
- [x] Create `app/prompts/` with outline, explain, draft, seo templates

### 1.8 Testing & Tooling
- [x] Create Makefile with dev commands
- [x] Create unit tests (12 tests passing)
- [x] Verify app starts and health check works

---

## Phase 2: Core Features [COMPLETED]

### 2.1 Pydantic Models
- [x] Create `app/models/requests.py` with all request schemas
- [x] Create `app/models/responses.py` with all response schemas

### 2.2 Outline Generation
- [x] Create `app/api/outline.py` router with LLM integration
- [x] Create `app/services/content_service.py` with generate_outline()
- [x] SEO-optimized title and section generation

### 2.3 Concept Explainer
- [x] Create `app/api/explain.py` router with LLM integration
- [x] ELI5, technical, and deep-dive modes
- [x] Code examples and analogies generation

### 2.4 Draft Writer
- [x] Create `app/api/draft.py` router with LLM integration
- [x] Tone customization and markdown output

### 2.5 Research Service
- [x] Create `app/services/research_service.py` with LLM integration
- [x] Topic research with findings and sources
- [x] Confidence scoring for findings

### 2.6 SEO Optimizer
- [x] Create `app/api/seo.py` router with LLM integration
- [x] Keyword analysis and meta description generation

### 2.7 Knowledge Base API (Placeholder)
- [x] Create `app/api/knowledge.py` router (endpoints ready, RAG pending)

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
