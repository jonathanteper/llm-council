# Product Backlog: LLM Council

**Version:** 1.0  
**Date:** December 24, 2025  
**Status:** Active  
**Owner:** Product Team

---

## Table of Contents

1. [Overview](#overview)
2. [v1.3 - API Hardening](#v13---api-hardening)
3. [v2.0 - Multi-App Ecosystem](#v20---multi-app-ecosystem)
4. [v2.1+ - Production Readiness](#v21---production-readiness)
5. [v3.0+ - Advanced Features](#v30---advanced-features)
6. [Future Exploration](#future-exploration)
7. [Technical Debt](#technical-debt)

---

## Overview

This backlog captures features, enhancements, and ideas that are out of scope for current versions but valuable for future development. Items are organized by target version with clear rationale and dependencies.

**Backlog Management:**
- Items marked with 🎯 are high priority for their version
- Items marked with 💡 are ideas requiring further validation
- Items marked with 🔧 are technical improvements
- Items marked with 📊 are analytics/observability features

---

## v1.3 - API Hardening

**Target:** Q1 2026  
**Focus:** Production-ready API improvements

### Rationale
Once external apps are actively using the API, these operational features become important for reliability, security, and monitoring.

### Features

#### 🎯 Rate Limiting
**Priority:** P0 (Must Have)  
**Effort:** Medium

**Description:**
Protect API from abuse and ensure fair usage across clients.

**Requirements:**
- Per-API-key rate limiting (when auth enabled)
- IP-based rate limiting (when auth disabled)
- Configurable limits per endpoint
- 429 response with Retry-After header
- Redis or in-memory storage

**Configuration:**
```bash
RATE_LIMIT_ENABLED=true
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_PER_HOUR=1000
```

**Dependencies:** None  
**Risks:** May impact legitimate high-volume users

---

#### 🎯 Request/Response Logging
**Priority:** P0 (Must Have)  
**Effort:** Small

**Description:**
Track all API requests for debugging and auditing.

**Requirements:**
- Log all requests with timestamp, method, path, status
- Include request ID for tracing
- Configurable log levels
- Rotate logs automatically
- Exclude sensitive data (API keys)

**Tech Stack:** Python logging, structured JSON logs

**Dependencies:** None  
**Risks:** Log volume growth

---

#### 📊 API Usage Analytics
**Priority:** P1 (Should Have)  
**Effort:** Medium

**Description:**
Monitor endpoint usage, performance, and trends.

**Requirements:**
- Endpoint hit counts
- Response time percentiles (p50, p95, p99)
- Error rate by endpoint
- Active API keys (when auth enabled)
- Simple dashboard or CSV export

**Tech Stack:** In-memory metrics, optional Prometheus export

**Dependencies:** Request logging  
**Risks:** Performance overhead

---

#### 🔧 Enhanced Error Responses
**Priority:** P1 (Should Have)  
**Effort:** Small

**Description:**
Provide more detailed error information for debugging.

**Current:**
```json
{"detail": "Invalid API key"}
```

**Enhanced:**
```json
{
  "error": {
    "code": "INVALID_API_KEY",
    "message": "The provided API key is invalid",
    "request_id": "abc-123",
    "timestamp": "2026-01-15T10:00:00Z",
    "docs_url": "http://localhost:8001/docs#authentication"
  }
}
```

**Dependencies:** None  
**Risks:** May expose too much information

---

#### 💡 Webhook Support
**Priority:** P2 (Nice to Have)  
**Effort:** Large

**Description:**
Notify external apps when events occur (conversation completed, etc.).

**Requirements:**
- Register webhook URLs per API key
- POST events to registered URLs
- Retry logic with exponential backoff
- Webhook signature validation (HMAC)
- Event types: `conversation.created`, `message.completed`

**Dependencies:** Auth system  
**Risks:** Complex implementation, reliability challenges

---

#### 🔧 API Key Management Endpoint
**Priority:** P2 (Nice to Have)  
**Effort:** Medium

**Description:**
CRUD operations for API keys via API.

**Endpoints:**
- `POST /api/v1/auth/keys` - Create new key
- `GET /api/v1/auth/keys` - List keys
- `DELETE /api/v1/auth/keys/{id}` - Revoke key
- `PUT /api/v1/auth/keys/{id}` - Update key metadata

**Dependencies:** Auth system, user accounts  
**Risks:** Security implications

---

#### 🔧 Deprecate Legacy Routes
**Priority:** P0 (Must Have)  
**Effort:** Small

**Description:**
Remove backward-compatibility aliases from v1.1.

**Action:**
- Remove `/api/conversations` → `/api/v1/conversations` aliases
- Announce 6 months in advance
- Update all internal code
- Add migration guide to docs

**Timeline:** Announce in v1.3, remove in v1.4

**Dependencies:** All external apps migrated  
**Risks:** Breaking change for unmigrated apps

---

## v2.0 - Multi-App Ecosystem

**Target:** Q2 2026  
**Focus:** Enable multiple apps with shared capabilities

### Rationale
Once multiple applications need to integrate with each other, shared services become valuable. Each service is optional and apps can choose what to use.

---

### 🎯 Shared Memory Service

**Priority:** P0 (Must Have)  
**Effort:** X-Large

**Description:**
Cross-app conversation context and semantic search.

**Project:** New Cursor project `llm-council-memory`

**Architecture:**
```
llm-council-memory/
├── backend/
│   ├── main.py          # FastAPI app
│   ├── vector_store.py  # Vector DB interface
│   └── models.py        # Data models
├── docker-compose.yml
└── README.md
```

**API Design:**
```
POST   /api/v1/memories              # Store memory
GET    /api/v1/memories/search       # Semantic search
GET    /api/v1/memories/{app_id}     # List by app
DELETE /api/v1/memories/{id}         # Delete memory
```

**Features:**
- Store conversation summaries with embeddings
- Semantic search across conversations
- Per-app namespacing (data isolation)
- Optional: Cross-app context sharing (explicit opt-in)
- Vector similarity search
- Metadata filtering (date, app, user)

**Tech Stack:**
- FastAPI backend
- Vector DB: ChromaDB, Pinecone, or Weaviate
- Embedding model: OpenAI or local

**Integration with Council:**
```python
# Optional memory retrieval before council query
context = await memory_service.search(query, app_id="council")
enhanced_query = f"Context: {context}\n\nQuery: {query}"
result = await run_full_council(enhanced_query)
```

**Configuration:**
```bash
MEMORY_SERVICE_ENABLED=true
MEMORY_SERVICE_URL=http://localhost:8002
```

**Dependencies:** None (standalone service)  
**Risks:** Complexity, vector DB management, embedding costs

---

### 🎯 Shared Authentication Service

**Priority:** P1 (Should Have)  
**Effort:** X-Large

**Description:**
Centralized user accounts and OAuth for multi-app ecosystem.

**Project:** New Cursor project `llm-council-auth`

**Architecture:**
```
llm-council-auth/
├── backend/
│   ├── main.py       # FastAPI app
│   ├── auth.py       # OAuth2 implementation
│   ├── users.py      # User management
│   └── tokens.py     # JWT handling
├── database/
│   └── init.sql      # User schema
└── README.md
```

**API Design:**
```
POST   /api/v1/auth/register         # User registration
POST   /api/v1/auth/login            # Login
POST   /api/v1/auth/token            # OAuth2 token
GET    /api/v1/auth/user/me          # Get user profile
POST   /api/v1/auth/refresh          # Refresh token
POST   /api/v1/auth/logout           # Logout
```

**Features:**
- User registration and login
- OAuth2 authorization code flow
- JWT token issuance and validation
- User profile management
- Email verification
- Password reset
- API key generation per user

**Tech Stack:**
- FastAPI backend
- PostgreSQL database
- JWT tokens
- bcrypt for passwords
- OAuth2 library

**Integration:**
Apps validate JWT tokens issued by auth service:
```python
token = request.headers.get("Authorization")
user = await auth_service.validate_token(token)
```

**Dependencies:** None (standalone service)  
**Risks:** Security-critical, complex OAuth flows

---

### 🎯 Model Context Protocol (MCP) Server

**Priority:** P1 (Should Have)  
**Effort:** Medium

**Description:**
Expose LLM Council as an MCP server, enabling AI assistants (Claude Desktop, etc.) to use the council as a tool.

**Project:** New component `llm-council-mcp`

**Architecture:**
```
llm-council-mcp/
├── src/
│   ├── index.ts          # MCP server implementation
│   ├── tools.ts          # Tool definitions
│   └── council-client.ts # Council API client
├── package.json
└── README.md
```

**MCP Tools Exposed:**
```typescript
// Tool 1: Query Council
{
  name: "query_council",
  description: "Get multi-perspective AI insights on any topic",
  inputSchema: {
    type: "object",
    properties: {
      question: {
        type: "string",
        description: "The question to ask the council"
      },
      streamUpdates: {
        type: "boolean",
        description: "Whether to stream deliberation updates"
      }
    }
  }
}

// Tool 2: Get Conversation History
{
  name: "get_conversation",
  description: "Retrieve a previous council conversation",
  inputSchema: {
    type: "object",
    properties: {
      conversationId: {
        type: "string",
        description: "The conversation ID to retrieve"
      }
    }
  }
}

// Tool 3: List Conversations
{
  name: "list_conversations",
  description: "List all council conversations",
  inputSchema: {
    type: "object",
    properties: {}
  }
}
```

**Usage Example:**
```json
// Claude Desktop config (claude_desktop_config.json)
{
  "mcpServers": {
    "llm-council": {
      "command": "node",
      "args": ["/path/to/llm-council-mcp/dist/index.js"],
      "env": {
        "COUNCIL_API_URL": "http://localhost:8001",
        "COUNCIL_API_KEY": "optional-key"
      }
    }
  }
}
```

**User Experience:**
```
User (in Claude Desktop): "Can you ask the LLM council about the future of AI?"

Claude: [Uses query_council tool]
  → Calls LLM Council API
  → Receives multi-model deliberation
  → Presents synthesis to user

Claude: "Based on the council's deliberation across GPT-5.1, Gemini-3, 
Claude-4.5, and Grok-4, here's a comprehensive view..."
```

**Features:**
- Expose council as MCP tool for AI assistants
- Support both streaming and non-streaming modes
- Pass through authentication if configured
- Error handling and retries
- Tool result formatting for AI consumption

**Tech Stack:**
- TypeScript/Node.js (MCP SDK is TypeScript-based)
- MCP SDK (@modelcontextprotocol/sdk)
- Council API client (HTTP)

**Integration Points:**
- Claude Desktop
- Other MCP-compatible AI assistants
- Custom MCP clients

**Configuration:**
```bash
# .env for MCP server
COUNCIL_API_URL=http://localhost:8001
COUNCIL_API_KEY=optional-key-here
MCP_SERVER_PORT=3000  # optional
LOG_LEVEL=info
```

**Benefits:**
- Makes council accessible to AI assistants
- Users can leverage council through natural conversation
- No custom UI needed for simple queries
- Enables "AI consulting AI" workflows

**Dependencies:** v1.2 API (already complete)  
**Risks:** MCP protocol changes, auth complexity

**Reference:**
- MCP Specification: https://modelcontextprotocol.io/
- Example servers: https://github.com/modelcontextprotocol/servers

---

### 💡 Service Discovery

**Priority:** P2 (Nice to Have)  
**Effort:** Medium

**Description:**
Apps find each other dynamically without hardcoded URLs.

**Approach:**
- Simple JSON config file or API-based registry
- Services register at startup
- Health checks and availability monitoring
- Load balancing information

**Registry API:**
```
POST   /api/v1/registry/services      # Register service
GET    /api/v1/registry/services      # List services
GET    /api/v1/registry/services/{id} # Get service info
DELETE /api/v1/registry/services/{id} # Deregister
```

**Service Info:**
```json
{
  "id": "llm-council",
  "name": "LLM Council API",
  "version": "2.0.0",
  "url": "http://localhost:8001",
  "status": "healthy",
  "endpoints": ["/api/v1/conversations", ...]
}
```

**Dependencies:** None  
**Risks:** Single point of failure

---

### 🔧 Multi-Tenancy Support

**Priority:** P2 (Nice to Have)  
**Effort:** Large

**Description:**
Support multiple organizations/teams in shared deployment.

**Features:**
- Tenant isolation (data, conversations, API keys)
- Tenant-specific configuration
- Usage tracking per tenant
- Tenant admin dashboard

**Dependencies:** Auth service  
**Risks:** Data isolation complexity

---

## v2.1+ - Production Readiness

**Target:** Q3 2026  
**Focus:** Production deployment patterns

---

### 🎯 Production Docker Images

**Priority:** P0 (Must Have)  
**Effort:** Medium

**Description:**
Multi-stage Dockerfiles optimized for production.

**Features:**
- Separate dev and prod Dockerfiles
- Minimal production images (Alpine Linux)
- Security hardening
- Non-root user
- Health check integration
- Secret management

**Dependencies:** None  
**Risks:** None

---

### 🎯 Cloud Deployment Guides

**Priority:** P0 (Must Have)  
**Effort:** Medium

**Description:**
Step-by-step guides for major cloud platforms.

**Platforms:**
- Fly.io (recommended for small deployments)
- Railway (easy deployment)
- AWS (ECS, RDS)
- Google Cloud (Cloud Run, Cloud SQL)
- Azure (Container Instances, Cosmos DB)

**Each guide includes:**
- Infrastructure as code (Terraform/CloudFormation)
- Environment variable configuration
- Database setup
- Monitoring setup
- Cost estimates

**Dependencies:** Production Docker images  
**Risks:** Maintenance burden

---

### 📊 Database Migration

**Priority:** P1 (Should Have)  
**Effort:** Large

**Description:**
Move from JSON files to PostgreSQL for reliability and scalability.

**Migration Path:**
1. Create database schema
2. Write migration script (JSON → PostgreSQL)
3. Add database config
4. Update storage layer
5. Keep JSON as backup/export format

**Schema:**
```sql
CREATE TABLE conversations (
    id UUID PRIMARY KEY,
    created_at TIMESTAMP,
    title TEXT,
    user_id UUID
);

CREATE TABLE messages (
    id UUID PRIMARY KEY,
    conversation_id UUID REFERENCES conversations(id),
    role VARCHAR(20),
    content JSONB,
    created_at TIMESTAMP
);
```

**Dependencies:** Production deployment  
**Risks:** Data migration complexity, testing burden

---

### 🎯 API Gateway

**Priority:** P1 (Should Have)  
**Effort:** Large

**Description:**
Single entry point for all services in ecosystem.

**Options:**
- Kong (feature-rich, proven)
- Tyk (open source, Go-based)
- Custom FastAPI gateway (lightweight)

**Features:**
- Request routing to services
- Centralized rate limiting
- Authentication/authorization
- Request transformation
- Response caching
- API versioning
- Monitoring and logging

**Architecture:**
```
Client → API Gateway → [Council, Memory, Auth services]
```

**Dependencies:** Multiple services (v2.0)  
**Risks:** Single point of failure, complexity

---

### 💡 Message Queue

**Priority:** P2 (Nice to Have)  
**Effort:** Large

**Description:**
Async communication between services.

**Tech Options:**
- RabbitMQ (mature, feature-rich)
- Redis Pub/Sub (simple, lightweight)
- Apache Kafka (high throughput)

**Use Cases:**
- Long-running council deliberations
- Background job processing
- Event-driven architecture
- Decoupled request/response

**Dependencies:** None  
**Risks:** Operational complexity

---

### 📊 Monitoring & Observability

**Priority:** P1 (Should Have)  
**Effort:** Large

**Description:**
Comprehensive monitoring for production systems.

**Components:**

**1. Distributed Tracing:**
- Jaeger or Zipkin
- Trace requests across services
- Performance bottleneck identification

**2. Centralized Logging:**
- ELK stack (Elasticsearch, Logstash, Kibana)
- or Loki + Grafana
- Aggregate logs from all services

**3. Metrics Collection:**
- Prometheus for metrics
- Grafana for visualization
- Alert manager for notifications

**Dashboards:**
- Service health overview
- Request rates and latencies
- Error rates
- Resource utilization
- Business metrics (conversations/day, etc.)

**Dependencies:** Production deployment  
**Risks:** Infrastructure costs, maintenance

---

### 🔧 Horizontal Scaling

**Priority:** P1 (Should Have)  
**Effort:** Medium

**Description:**
Run multiple instances of services for high availability.

**Requirements:**
- Stateless services (already done)
- Load balancer (nginx, HAProxy, cloud LB)
- Shared database (PostgreSQL)
- Shared cache (Redis)
- Session management

**Configuration:**
```yaml
# docker-compose.yml
services:
  council:
    image: llm-council:2.0
    deploy:
      replicas: 3
    depends_on:
      - postgres
      - redis
```

**Dependencies:** Database migration, production deployment  
**Risks:** Session management, data consistency

---

## v3.0+ - Advanced Features

**Target:** 2027+  
**Focus:** Enhanced capabilities for mature ecosystem

---

### 💡 GraphQL API

**Priority:** P2 (Nice to Have)  
**Effort:** Large

**Description:**
Alternative to REST API with flexible queries.

**Rationale:**
- Reduce over-fetching
- Single request for complex data
- Real-time subscriptions
- Strong typing

**Tech Stack:**
- Strawberry or Ariadne (Python GraphQL)
- Alongside existing REST API (not replacing)

**Example Query:**
```graphql
query {
  conversation(id: "abc123") {
    title
    messages(last: 5) {
      role
      content {
        stage3 {
          response
        }
      }
    }
  }
}
```

**Dependencies:** None  
**Risks:** Complexity, caching challenges

---

### 💡 WebSocket Support

**Priority:** P2 (Nice to Have)  
**Effort:** Medium

**Description:**
Bi-directional real-time communication.

**Use Cases:**
- Live council deliberation updates
- Chat-style interface
- Collaborative features
- Push notifications

**Tech Stack:**
- FastAPI WebSocket support
- Socket.IO (if needed for broad client support)

**Dependencies:** None  
**Risks:** Connection management, scaling

---

### 💡 Advanced Caching

**Priority:** P2 (Nice to Have)  
**Effort:** Medium

**Description:**
Intelligent response caching to reduce API calls and costs.

**Features:**
- Cache similar queries (semantic similarity)
- Configurable TTL per query type
- Cache invalidation strategies
- Redis or in-memory cache

**Example:**
```python
# Cache responses for repeated questions
if similar_query_cached(query):
    return cached_response
```

**Dependencies:** Vector search (for semantic similarity)  
**Risks:** Stale data, cache invalidation complexity

---

### 💡 Model Provider Abstraction

**Priority:** P2 (Nice to Have)  
**Effort:** Large

**Description:**
Support multiple LLM providers beyond OpenRouter.

**Providers:**
- Direct OpenAI API
- Direct Anthropic API
- Azure OpenAI
- Google Vertex AI
- AWS Bedrock
- Local models (Ollama)

**Config:**
```yaml
models:
  - provider: openai
    model: gpt-4
    api_key: ${OPENAI_KEY}
  - provider: anthropic
    model: claude-3
    api_key: ${ANTHROPIC_KEY}
```

**Dependencies:** None  
**Risks:** API incompatibilities, testing burden

---

## Future Exploration

Ideas requiring validation and research.

### 💡 Fine-Tuned Council Models

Train models specifically for council deliberation roles.

**Research Needed:**
- Is fine-tuning better than prompting?
- Cost/benefit analysis
- Data collection strategy

---

### 💡 Conversation Summarization

Auto-summarize long conversations for context efficiency.

**Use Cases:**
- Reduce token usage
- Faster context loading
- Better long-term memory

---

### 💡 Multi-Modal Support

Support images, audio, documents in queries.

**Challenges:**
- Model availability
- UI complexity
- Storage requirements

---

### 💡 Council Orchestration Options

Let users choose council size, models, voting mechanisms.

**Options:**
- Small council (3 models, fast)
- Large council (10 models, comprehensive)
- Custom model selection
- Weighted voting

---

### 💡 A/B Testing Framework

Compare different council configurations.

**Metrics:**
- Response quality
- Speed
- Cost
- User satisfaction

---

## Technical Debt

Items that should be addressed to maintain code quality.

### 🔧 Test Coverage Gaps

**Current:** 90% backend, 70% frontend  
**Target:** 95% backend, 85% frontend

**Actions:**
- Add missing unit tests
- Improve edge case coverage
- Add more E2E tests

**Priority:** P1  
**Effort:** Medium

---

### 🔧 Error Handling Standardization

Ensure all endpoints use consistent error format.

**Priority:** P1  
**Effort:** Small

---

### 🔧 Configuration Management

Move from environment variables to configuration files for complex setups.

**Options:**
- YAML config files
- Config validation
- Config hot-reload

**Priority:** P2  
**Effort:** Medium

---

### 🔧 Code Documentation

Improve inline documentation and docstrings.

**Priority:** P2  
**Effort:** Small

---

### 🔧 Dependency Updates

Regular updates to keep dependencies current.

**Schedule:** Monthly review  
**Priority:** P1 (security), P2 (features)

---

## Backlog Management Process

### Adding Items

1. Create detailed description
2. Assign priority (P0-P3)
3. Estimate effort (Small/Medium/Large/X-Large)
4. Identify dependencies and risks
5. Link to related PRDs or issues

### Prioritizing Items

**Factors:**
- User value
- Technical dependencies
- Resource availability
- Strategic alignment
- Risk mitigation

### Moving to Active Development

When a backlog item is ready:
1. Create version PRD (e.g., PRD-v1.3.md)
2. Break down into detailed requirements
3. Create technical specification
4. Add to current sprint/version

---

## Related Documents

- [Project Conventions](./ProjectConventions.md)
- [Product Overview](./ProductOverview.md)
- [Version PRDs](./versions/)

---

**Last Updated:** December 24, 2025  
**Next Review:** End of v1.2 release

