# Implementation Plan: LLM Council v1.2 - API-Ready Architecture

**Version:** 1.2  
**Date:** December 24, 2025  
**Status:** Draft  
**Estimated Duration:** 3 weeks

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Phase 1: API Versioning](#phase-1-api-versioning)
4. [Phase 2: External Access](#phase-2-external-access)
5. [Phase 3: Documentation](#phase-3-documentation)
6. [Phase 4: Optional Authentication](#phase-4-optional-authentication)
7. [Phase 5: Validation](#phase-5-validation)
8. [Testing & Validation](#testing--validation)
9. [Rollback Strategy](#rollback-strategy)
10. [Post-Implementation](#post-implementation)

---

## Overview

This document provides a step-by-step guide for implementing API-ready architecture for LLM Council v1.2. The implementation maintains 100% backward compatibility while enabling external application integration.

### Implementation Approach

- **Incremental:** Build and test each component before moving to next
- **Non-Breaking:** Existing web UI continues working unchanged
- **Validated:** Test after each phase to catch issues early
- **Documented:** Update documentation as we go

### Success Criteria

By the end of implementation:
- ✅ All API routes versioned under `/api/v1/`
- ✅ CORS configured for cross-origin requests
- ✅ Optional API key authentication working
- ✅ `/api/v1/status` endpoint operational
- ✅ README_API.md complete with examples
- ✅ All v1.1 functionality preserved
- ✅ 100% backward compatibility maintained

---

## Prerequisites

### System Requirements

**Required Software:**
- [ ] **Python 3.10+** with uv package manager
- [ ] **Node.js 20+** with npm
- [ ] **Docker & OrbStack** (v1.1 completed)
- [ ] **Git** for version control
- [ ] **curl** or **Postman** for API testing

**Verify v1.1 Setup:**
```bash
# Check Docker is running
docker compose ps
# Expected: backend and frontend running

# Check application is working
open http://localhost:5173
# Expected: App loads and works

# Check current API endpoints
curl http://localhost:8001/api/conversations
# Expected: JSON response with conversations list
```

### Project Requirements

**Current State:**
- [ ] v1.1 Docker setup complete and working
- [ ] All v1.1 tests passing
- [ ] `.env` file with valid `OPENROUTER_API_KEY`
- [ ] Existing conversations can be created and viewed

**Backup (Recommended):**
```bash
# Create checkpoint before starting
git add -A
git commit -m "chore: Pre-v1.2 checkpoint - v1.1 stable"

# Or create a branch
git checkout -b feature/api-ready-v1.2
```

---

## Phase 1: API Versioning

**Goal:** Add `/api/v1/` prefix to all API endpoints while maintaining backward compatibility.

**Duration:** Week 1 (Days 1-2)

### Step 1.1: Create API Router Structure

**Create directory structure:**
```bash
mkdir -p backend/routers
touch backend/routers/__init__.py
touch backend/routers/api_v1.py
```

**Create `backend/routers/api_v1.py`:**
```python
"""API v1 routes for LLM Council."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import uuid

from .. import storage
from ..council import run_full_council, generate_conversation_title
from ..council import stage1_collect_responses, stage2_collect_rankings
from ..council import stage3_synthesize_final, calculate_aggregate_rankings

# Create v1 router with prefix
router = APIRouter(prefix="/api/v1", tags=["v1"])


class CreateConversationRequest(BaseModel):
    """Request to create a new conversation."""
    pass


class SendMessageRequest(BaseModel):
    """Request to send a message in a conversation."""
    content: str


class ConversationMetadata(BaseModel):
    """Conversation metadata for list view."""
    id: str
    created_at: str
    title: str
    message_count: int


class Conversation(BaseModel):
    """Full conversation with all messages."""
    id: str
    created_at: str
    title: str
    messages: List[Dict[str, Any]]


@router.get("/conversations", response_model=List[ConversationMetadata])
async def list_conversations():
    """List all conversations (API v1)."""
    return storage.list_conversations()


@router.post("/conversations", response_model=Conversation)
async def create_conversation(request: CreateConversationRequest):
    """Create a new conversation (API v1)."""
    conversation_id = str(uuid.uuid4())
    conversation = storage.create_conversation(conversation_id)
    return conversation


@router.get("/conversations/{conversation_id}", response_model=Conversation)
async def get_conversation(conversation_id: str):
    """Get a specific conversation with all its messages (API v1)."""
    conversation = storage.get_conversation(conversation_id)
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation


@router.post("/conversations/{conversation_id}/message")
async def send_message(conversation_id: str, request: SendMessageRequest):
    """
    Send a message and run the 3-stage council process (API v1).
    Returns the complete response with all stages.
    """
    # Check if conversation exists
    conversation = storage.get_conversation(conversation_id)
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # Check if this is the first message
    is_first_message = len(conversation["messages"]) == 0

    # Add user message
    storage.add_user_message(conversation_id, request.content)

    # If this is the first message, generate a title
    if is_first_message:
        title = await generate_conversation_title(request.content)
        storage.update_conversation_title(conversation_id, title)

    # Run the 3-stage council process
    stage1_results, stage2_results, stage3_result, metadata = await run_full_council(
        request.content
    )

    # Add assistant message with all stages
    storage.add_assistant_message(
        conversation_id,
        stage1_results,
        stage2_results,
        stage3_result
    )

    # Return the complete response with metadata
    return {
        "stage1": stage1_results,
        "stage2": stage2_results,
        "stage3": stage3_result,
        "metadata": metadata
    }


@router.post("/conversations/{conversation_id}/message/stream")
async def send_message_stream(conversation_id: str, request: SendMessageRequest):
    """
    Send a message and stream the 3-stage council process (API v1).
    Returns Server-Sent Events as each stage completes.
    """
    from fastapi.responses import StreamingResponse
    import json
    import asyncio
    
    # Check if conversation exists
    conversation = storage.get_conversation(conversation_id)
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # Check if this is the first message
    is_first_message = len(conversation["messages"]) == 0

    async def event_generator():
        try:
            # Add user message
            storage.add_user_message(conversation_id, request.content)

            # Start title generation in parallel (don't await yet)
            title_task = None
            if is_first_message:
                title_task = asyncio.create_task(generate_conversation_title(request.content))

            # Stage 1: Collect responses
            yield f"data: {json.dumps({'type': 'stage1_start'})}\n\n"
            stage1_results = await stage1_collect_responses(request.content)
            yield f"data: {json.dumps({'type': 'stage1_complete', 'data': stage1_results})}\n\n"

            # Stage 2: Collect rankings
            yield f"data: {json.dumps({'type': 'stage2_start'})}\n\n"
            stage2_results, label_to_model = await stage2_collect_rankings(request.content, stage1_results)
            aggregate_rankings = calculate_aggregate_rankings(stage2_results, label_to_model)
            yield f"data: {json.dumps({'type': 'stage2_complete', 'data': stage2_results, 'metadata': {'label_to_model': label_to_model, 'aggregate_rankings': aggregate_rankings}})}\n\n"

            # Stage 3: Synthesize final answer
            yield f"data: {json.dumps({'type': 'stage3_start'})}\n\n"
            stage3_result = await stage3_synthesize_final(request.content, stage1_results, stage2_results)
            yield f"data: {json.dumps({'type': 'stage3_complete', 'data': stage3_result})}\n\n"

            # Wait for title generation if it was started
            if title_task:
                title = await title_task
                storage.update_conversation_title(conversation_id, title)
                yield f"data: {json.dumps({'type': 'title_complete', 'data': {'title': title}})}\n\n"

            # Save complete assistant message
            storage.add_assistant_message(
                conversation_id,
                stage1_results,
                stage2_results,
                stage3_result
            )

            # Send completion event
            yield f"data: {json.dumps({'type': 'complete'})}\n\n"

        except Exception as e:
            # Send error event
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )


@router.get("/status")
async def get_status():
    """
    Get service status and metadata (API v1).
    
    Returns information about the service, available models, and features.
    """
    from ..config import COUNCIL_MODELS, CHAIRMAN_MODEL
    
    return {
        "service": "LLM Council API",
        "version": "1.2.0",
        "api_version": "v1",
        "status": "healthy",
        "models": {
            "council": COUNCIL_MODELS,
            "chairman": CHAIRMAN_MODEL
        },
        "features": {
            "auth_required": False,  # Will be dynamic in Step 4.2
            "streaming": True,
            "versioned_api": True
        }
    }
```

**Commit:**
```bash
git add backend/routers/
git commit -m "feat: Add v1 API router with versioned endpoints (FR-2.1)"
```

### Step 1.2: Register Router in Main App

**Modify `backend/main.py`:**
```python
"""FastAPI backend for LLM Council."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import v1 router
from .routers import api_v1

app = FastAPI(title="LLM Council API")

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint."""
    return {"status": "ok", "service": "LLM Council API"}


@app.get("/health")
async def health_check():
    """
    Health check endpoint for Docker container orchestration.
    
    Implements: [v1.1-FR-1.3] (Backend Health Check)
    
    Returns service status for Docker health checks and monitoring.
    """
    return {"status": "healthy", "service": "LLM Council API"}


# Register v1 API router
app.include_router(api_v1.router)


# Backward compatibility aliases (temporary - remove in v1.3)
@app.get("/api/conversations")
async def list_conversations_legacy():
    """DEPRECATED: Use /api/v1/conversations instead."""
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/api/v1/conversations", status_code=301)


@app.post("/api/conversations")
async def create_conversation_legacy():
    """DEPRECATED: Use /api/v1/conversations instead."""
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/api/v1/conversations", status_code=307)


@app.get("/api/conversations/{conversation_id}")
async def get_conversation_legacy(conversation_id: str):
    """DEPRECATED: Use /api/v1/conversations/{id} instead."""
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url=f"/api/v1/conversations/{conversation_id}", status_code=301)


@app.post("/api/conversations/{conversation_id}/message")
async def send_message_legacy(conversation_id: str):
    """DEPRECATED: Use /api/v1/conversations/{id}/message instead."""
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url=f"/api/v1/conversations/{conversation_id}/message", status_code=307)


@app.post("/api/conversations/{conversation_id}/message/stream")
async def send_message_stream_legacy(conversation_id: str):
    """DEPRECATED: Use /api/v1/conversations/{id}/message/stream instead."""
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url=f"/api/v1/conversations/{conversation_id}/message/stream", status_code=307)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
```

**Commit:**
```bash
git add backend/main.py
git commit -m "feat: Register v1 router and add backward compatibility aliases (FR-2.1, FR-4.1)"
```

### Step 1.3: Test Versioned API Endpoints

**Test commands:**
```bash
# Start services
docker compose up -d

# Test v1 endpoints
curl http://localhost:8001/api/v1/status
curl http://localhost:8001/api/v1/conversations

# Test backward compatibility (should redirect)
curl -I http://localhost:8001/api/conversations
# Expected: 301 redirect to /api/v1/conversations
```

### Step 1.4: Update Frontend to Use v1 Routes

**Modify `frontend/src/api.js`:**
```javascript
// Update base URL to use versioned API
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001';
const API_V1 = `${API_BASE_URL}/api/v1`;

export async function getConversations() {
  const response = await fetch(`${API_V1}/conversations`);
  if (!response.ok) throw new Error('Failed to fetch conversations');
  return response.json();
}

export async function createConversation() {
  const response = await fetch(`${API_V1}/conversations`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({})
  });
  if (!response.ok) throw new Error('Failed to create conversation');
  return response.json();
}

export async function getConversation(id) {
  const response = await fetch(`${API_V1}/conversations/${id}`);
  if (!response.ok) throw new Error('Failed to fetch conversation');
  return response.json();
}

export async function sendMessage(conversationId, content) {
  const response = await fetch(`${API_V1}/conversations/${conversationId}/message/stream`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ content })
  });
  if (!response.ok) throw new Error('Failed to send message');
  return response;
}
```

**Commit:**
```bash
git add frontend/src/api.js
git commit -m "feat: Update frontend to use v1 API endpoints (FR-4.1)"
```

### Step 1.5: Test Frontend with v1 API

**Manual testing:**
1. Open http://localhost:5173
2. Create a new conversation
3. Send a message to council
4. Verify all stages work
5. Check browser network tab shows `/api/v1/` URLs

**Verification:**
```bash
# Check backend logs for v1 route hits
docker compose logs backend | grep "api/v1"
```

---

## Phase 2: External Access

**Goal:** Configure CORS and add service status endpoint for external apps.

**Duration:** Week 1-2 (Days 3-5)

### Step 2.1: Create CORS Configuration Module

**Create `backend/middleware/__init__.py`:**
```python
"""Middleware modules for LLM Council API."""
```

**Create `backend/middleware/cors.py`:**
```python
"""CORS configuration for API."""

import os
from typing import List


def get_cors_origins() -> List[str]:
    """
    Load CORS origins from environment variable.
    
    Returns:
        List of allowed origins, or ["*"] for wildcard
    """
    origins_str = os.getenv(
        "API_CORS_ORIGINS",
        "http://localhost:5173,http://localhost:3000"
    )
    
    # Support wildcard
    if origins_str == "*":
        return ["*"]
    
    # Parse comma-separated list
    origins = [o.strip() for o in origins_str.split(",") if o.strip()]
    return origins if origins else ["*"]
```

**Commit:**
```bash
git add backend/middleware/
git commit -m "feat: Add CORS configuration module (FR-1.1)"
```

### Step 2.2: Update CORS Middleware in Main App

**Modify `backend/main.py`:**
```python
from .middleware.cors import get_cors_origins

# ... (after app creation)

# Configure CORS with environment-based origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-API-Version", "X-Service-Version"],
)
```

**Commit:**
```bash
git add backend/main.py
git commit -m "feat: Use configurable CORS origins (FR-1.1)"
```

### Step 2.3: Add Version Headers Middleware

**Create `backend/middleware/versioning.py`:**
```python
"""API versioning middleware."""

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class VersionHeadersMiddleware(BaseHTTPMiddleware):
    """Add version information to response headers."""
    
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-API-Version"] = "v1"
        response.headers["X-Service-Version"] = "1.2.0"
        return response
```

**Register in `backend/main.py`:**
```python
from .middleware.versioning import VersionHeadersMiddleware

# ... (after CORS middleware)

# Add version headers to all responses
app.add_middleware(VersionHeadersMiddleware)
```

**Commit:**
```bash
git add backend/middleware/versioning.py backend/main.py
git commit -m "feat: Add version headers to API responses (FR-2.2)"
```

### Step 2.4: Test Cross-Origin Requests

**Create test HTML file `test-cors.html`:**
```html
<!DOCTYPE html>
<html>
<head>
    <title>CORS Test</title>
</head>
<body>
    <h1>LLM Council CORS Test</h1>
    <button onclick="testAPI()">Test API Call</button>
    <pre id="result"></pre>
    
    <script>
        async function testAPI() {
            try {
                const response = await fetch('http://localhost:8001/api/v1/status');
                const data = await response.json();
                document.getElementById('result').textContent = JSON.stringify(data, null, 2);
            } catch (error) {
                document.getElementById('result').textContent = 'Error: ' + error.message;
            }
        }
    </script>
</body>
</html>
```

**Test:**
```bash
# Serve on different port
python3 -m http.server 8080

# Open http://localhost:8080/test-cors.html
# Click button - should work without CORS errors
```

### Step 2.5: Update .env.example

**Create `.env.example`:**
```bash
# Required
OPENROUTER_API_KEY=sk-or-v1-your-key-here

# Optional (v1.2)
API_CORS_ORIGINS=http://localhost:5173,http://localhost:3000
# API_CORS_ORIGINS=*  # Allow all origins (dev only)

# Optional (v1.2 - Phase 4)
# API_KEYS=key1,key2,key3
```

**Commit:**
```bash
git add .env.example test-cors.html
git commit -m "docs: Add CORS example and .env.example for v1.2 (FR-1.1)"
```

---

## Phase 3: Documentation

**Goal:** Create comprehensive API documentation for external developers.

**Duration:** Week 2 (Days 1-3)

### Step 3.1: Create README_API.md

**Create `README_API.md` in project root:**

```markdown
# LLM Council API Documentation

Version: 1.2.0  
API Version: v1

## Quick Start

The LLM Council API allows you to integrate multi-perspective AI deliberation into your applications.

### Base URL

```
http://localhost:8001/api/v1
```

### Authentication (Optional)

Include `X-API-Key` header if authentication is enabled:

```http
X-API-Key: your-api-key-here
```

---

## Endpoints

### GET /status

Get service information and available models.

**Example:**
```bash
curl http://localhost:8001/api/v1/status
```

**Response:**
```json
{
  "service": "LLM Council API",
  "version": "1.2.0",
  "api_version": "v1",
  "status": "healthy",
  "models": {
    "council": ["openai/gpt-5.1", ...],
    "chairman": "google/gemini-3-pro-preview"
  },
  "features": {
    "auth_required": false,
    "streaming": true,
    "versioned_api": true
  }
}
```

---

### POST /conversations

Create a new conversation.

**Request:**
```bash
curl -X POST http://localhost:8001/api/v1/conversations \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "created_at": "2025-12-24T10:30:00.123Z",
  "title": "New Conversation",
  "messages": []
}
```

---

### POST /conversations/{id}/message

Send a message to the council and get response.

**Request:**
```bash
curl -X POST http://localhost:8001/api/v1/conversations/YOUR_CONVERSATION_ID/message \
  -H "Content-Type: application/json" \
  -d '{"content": "What is quantum computing?"}'
```

**Response:**
```json
{
  "stage1": [
    {
      "model": "openai/gpt-5.1",
      "response": "Quantum computing is..."
    }
  ],
  "stage2": [...],
  "stage3": {
    "model": "google/gemini-3-pro-preview",
    "response": "Based on the council's insights..."
  },
  "metadata": {...}
}
```

---

## Code Examples

### Python

```python
import requests

API_BASE = "http://localhost:8001/api/v1"
headers = {"X-API-Key": "your-key-here"}  # Optional

# Create conversation
response = requests.post(f"{API_BASE}/conversations", headers=headers)
conversation = response.json()
conversation_id = conversation["id"]

# Send message
response = requests.post(
    f"{API_BASE}/conversations/{conversation_id}/message",
    json={"content": "What is quantum computing?"},
    headers=headers
)
result = response.json()
print(result["stage3"]["response"])
```

### JavaScript

```javascript
const API_BASE = "http://localhost:8001/api/v1";
const headers = {
  "Content-Type": "application/json",
  "X-API-Key": "your-key-here"  // Optional
};

// Create conversation
const createResponse = await fetch(`${API_BASE}/conversations`, {
  method: "POST",
  headers
});
const conversation = await createResponse.json();

// Send message
const messageResponse = await fetch(
  `${API_BASE}/conversations/${conversation.id}/message`,
  {
    method: "POST",
    headers,
    body: JSON.stringify({
      content: "What is quantum computing?"
    })
  }
);
const result = await messageResponse.json();
console.log(result.stage3.response);
```

---

## Error Handling

All errors follow this format:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable message",
    "details": {}
  }
}
```

### Common Error Codes

| HTTP Status | Error Code | Meaning |
|-------------|-----------|---------|
| 400 | `INVALID_REQUEST` | Request validation failed |
| 401 | `MISSING_API_KEY` | API key required but not provided |
| 401 | `INVALID_API_KEY` | API key invalid |
| 404 | `CONVERSATION_NOT_FOUND` | Conversation doesn't exist |
| 500 | `INTERNAL_ERROR` | Server error |

---

## API Versioning

- Current version: `v1`
- Version in URL: `/api/v1/...`
- Version in headers: `X-API-Version: v1`

Future versions will use `/api/v2/`, `/api/v3/`, etc.

---

## Rate Limits

Currently no rate limits. May be added in future versions.

---

## Support

- Documentation: https://github.com/your-repo
- Issues: https://github.com/your-repo/issues
```

**Commit:**
```bash
git add README_API.md
git commit -m "docs: Add comprehensive API documentation (FR-3.1)"
```

### Step 3.2: Enhance OpenAPI Descriptions

**Update router descriptions in `backend/routers/api_v1.py`:**
```python
router = APIRouter(
    prefix="/api/v1",
    tags=["v1"],
    responses={404: {"description": "Not found"}},
)

@router.get(
    "/conversations",
    response_model=List[ConversationMetadata],
    summary="List all conversations",
    description="""
    Retrieve a list of all conversations with metadata.
    
    Returns conversation ID, creation timestamp, title, and message count.
    Conversations are ordered by creation time (newest first).
    """,
    response_description="List of conversation metadata objects"
)
async def list_conversations():
    """List all conversations (API v1)."""
    return storage.list_conversations()
```

**Commit:**
```bash
git add backend/routers/api_v1.py
git commit -m "docs: Add OpenAPI descriptions to endpoints (FR-3.2)"
```

### Step 3.3: Update Main README

**Add API section to `README.md`:**
```markdown
## Using as an API

LLM Council can be used as an API by other applications.

### API Documentation

See [README_API.md](./README_API.md) for complete API documentation.

### Quick Example

```python
import requests

# Create conversation
response = requests.post("http://localhost:8001/api/v1/conversations")
conversation_id = response.json()["id"]

# Send message
response = requests.post(
    f"http://localhost:8001/api/v1/conversations/{conversation_id}/message",
    json={"content": "What is AI?"}
)
print(response.json()["stage3"]["response"])
```

### API Features

- **Versioned API**: All endpoints under `/api/v1/`
- **CORS Enabled**: Cross-origin requests supported
- **Optional Auth**: API key authentication available
- **Streaming**: Real-time streaming of council deliberation
```

**Commit:**
```bash
git add README.md
git commit -m "docs: Add API section to main README (FR-3.1)"
```

---

## Phase 4: Optional Authentication

**Goal:** Implement optional API key authentication without breaking existing usage.

**Duration:** Week 2-3 (Days 4-7)

### Step 4.1: Create Auth Middleware Module

**Create `backend/auth.py`:**
```python
"""Authentication middleware for API."""

import os
from typing import Optional
from fastapi import Header, HTTPException


def get_api_keys() -> list[str]:
    """
    Load API keys from environment variable.
    
    Returns:
        List of valid API keys, or empty list if auth disabled
    """
    keys_str = os.getenv("API_KEYS", "")
    if not keys_str:
        return []
    return [k.strip() for k in keys_str.split(",") if k.strip()]


async def verify_api_key(
    x_api_key: Optional[str] = Header(None)
) -> Optional[str]:
    """
    Verify API key if authentication is enabled.
    
    If API_KEYS environment variable is not set, authentication is disabled
    and this function allows all requests.
    
    Args:
        x_api_key: API key from X-API-Key header
        
    Returns:
        The validated API key, or None if auth disabled
        
    Raises:
        HTTPException: 401 if auth enabled and key invalid/missing
    """
    valid_keys = get_api_keys()
    
    # Auth disabled - allow all requests
    if not valid_keys:
        return None
    
    # Auth enabled but no key provided
    if not x_api_key:
        raise HTTPException(
            status_code=401,
            detail={
                "error": {
                    "code": "MISSING_API_KEY",
                    "message": "API key required. Provide X-API-Key header.",
                    "details": {
                        "header": "X-API-Key",
                        "documentation": "http://localhost:8001/api/v1/docs"
                    }
                }
            }
        )
    
    # Validate key
    if x_api_key not in valid_keys:
        raise HTTPException(
            status_code=401,
            detail={
                "error": {
                    "code": "INVALID_API_KEY",
                    "message": "The provided API key is invalid.",
                    "details": {}
                }
            }
        )
    
    return x_api_key
```

**Commit:**
```bash
git add backend/auth.py
git commit -m "feat: Add optional API key authentication middleware (FR-1.2)"
```

### Step 4.2: Add Auth to API Routes

**Update `backend/routers/api_v1.py`:**
```python
from fastapi import Depends
from typing import Optional
from ..auth import verify_api_key

# Add to all endpoints
@router.get("/conversations", response_model=List[ConversationMetadata])
async def list_conversations(
    api_key: Optional[str] = Depends(verify_api_key)
):
    """List all conversations (API v1). Optional auth."""
    return storage.list_conversations()

# Repeat for all other endpoints...
```

**Update status endpoint to show auth state:**
```python
@router.get("/status")
async def get_status():
    """Get service status and metadata (API v1)."""
    from ..config import COUNCIL_MODELS, CHAIRMAN_MODEL
    from ..auth import get_api_keys
    
    auth_enabled = len(get_api_keys()) > 0
    
    return {
        "service": "LLM Council API",
        "version": "1.2.0",
        "api_version": "v1",
        "status": "healthy",
        "models": {
            "council": COUNCIL_MODELS,
            "chairman": CHAIRMAN_MODEL
        },
        "features": {
            "auth_required": auth_enabled,
            "streaming": True,
            "versioned_api": True
        }
    }
```

**Commit:**
```bash
git add backend/routers/api_v1.py
git commit -m "feat: Add authentication dependency to all v1 endpoints (FR-1.2)"
```

### Step 4.3: Test Authentication

**Test auth disabled (default):**
```bash
# Should work without API key
curl http://localhost:8001/api/v1/conversations
```

**Test auth enabled:**
```bash
# Add to .env
echo "API_KEYS=testkey1,testkey2" >> .env

# Restart backend
docker compose restart backend

# Should fail without key
curl http://localhost:8001/api/v1/conversations
# Expected: 401 MISSING_API_KEY

# Should work with valid key
curl -H "X-API-Key: testkey1" http://localhost:8001/api/v1/conversations
# Expected: 200 OK

# Should fail with invalid key
curl -H "X-API-Key: wrongkey" http://localhost:8001/api/v1/conversations
# Expected: 401 INVALID_API_KEY

# Remove from .env for now
# (Keep auth disabled for backward compatibility)
```

### Step 4.4: Update Documentation

**Update `README_API.md` authentication section:**
```markdown
## Authentication

Authentication is **optional** and disabled by default.

### Enabling Authentication

Set the `API_KEYS` environment variable:

```bash
# .env file
API_KEYS=key1,key2,key3
```

### Using API Keys

Include the `X-API-Key` header in requests:

```bash
curl -H "X-API-Key: your-key-here" \
  http://localhost:8001/api/v1/conversations
```

### Checking Auth Status

```bash
curl http://localhost:8001/api/v1/status
```

Look for `"auth_required": true` in the response.
```

**Commit:**
```bash
git add README_API.md
git commit -m "docs: Update API documentation with auth instructions (FR-1.2)"
```

---

## Phase 5: Validation

**Goal:** Validate all functionality and build external test app.

**Duration:** Week 3 (Days 1-5)

### Step 5.1: Create Minimal Test Frontend

**Create `test-app/index.html`:**
```html
<!DOCTYPE html>
<html>
<head>
    <title>LLM Council API Test</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
        button { padding: 10px 20px; margin: 10px 0; }
        pre { background: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; }
        .error { color: red; }
        .success { color: green; }
    </style>
</head>
<body>
    <h1>LLM Council API Test</h1>
    
    <h2>1. Check Status</h2>
    <button onclick="checkStatus()">Check Status</button>
    <pre id="status-result"></pre>
    
    <h2>2. Create Conversation</h2>
    <button onclick="createConversation()">Create Conversation</button>
    <pre id="create-result"></pre>
    
    <h2>3. Send Message</h2>
    <input type="text" id="conversation-id" placeholder="Conversation ID" style="width: 300px;">
    <input type="text" id="message" placeholder="Your message" style="width: 300px;">
    <button onclick="sendMessage()">Send Message</button>
    <pre id="message-result"></pre>
    
    <script>
        const API_BASE = 'http://localhost:8001/api/v1';
        
        async function checkStatus() {
            try {
                const response = await fetch(`${API_BASE}/status`);
                const data = await response.json();
                document.getElementById('status-result').textContent = JSON.stringify(data, null, 2);
                document.getElementById('status-result').className = 'success';
            } catch (error) {
                document.getElementById('status-result').textContent = 'Error: ' + error.message;
                document.getElementById('status-result').className = 'error';
            }
        }
        
        async function createConversation() {
            try {
                const response = await fetch(`${API_BASE}/conversations`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({})
                });
                const data = await response.json();
                document.getElementById('create-result').textContent = JSON.stringify(data, null, 2);
                document.getElementById('create-result').className = 'success';
                document.getElementById('conversation-id').value = data.id;
            } catch (error) {
                document.getElementById('create-result').textContent = 'Error: ' + error.message;
                document.getElementById('create-result').className = 'error';
            }
        }
        
        async function sendMessage() {
            const conversationId = document.getElementById('conversation-id').value;
            const message = document.getElementById('message').value;
            
            if (!conversationId || !message) {
                alert('Please provide both conversation ID and message');
                return;
            }
            
            try {
                const response = await fetch(`${API_BASE}/conversations/${conversationId}/message`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ content: message })
                });
                const data = await response.json();
                document.getElementById('message-result').textContent = JSON.stringify(data, null, 2);
                document.getElementById('message-result').className = 'success';
            } catch (error) {
                document.getElementById('message-result').textContent = 'Error: ' + error.message;
                document.getElementById('message-result').className = 'error';
            }
        }
    </script>
</body>
</html>
```

**Test:**
```bash
cd test-app
python3 -m http.server 8080
# Open http://localhost:8080
# Test all three functions
```

**Commit:**
```bash
git add test-app/
git commit -m "test: Add minimal test frontend for API validation"
```

### Step 5.2: Run Full Validation Checklist

See [Testing & Validation](#testing--validation) section below.

### Step 5.3: Performance Benchmarking

**Create `test-app/benchmark.py`:**
```python
import requests
import time
import statistics

API_BASE = "http://localhost:8001/api/v1"

def benchmark_endpoint(url, method="GET", iterations=100):
    """Benchmark API endpoint."""
    times = []
    for i in range(iterations):
        start = time.time()
        if method == "GET":
            response = requests.get(url)
        else:
            response = requests.post(url, json={})
        elapsed = (time.time() - start) * 1000  # ms
        times.append(elapsed)
        
        if i % 10 == 0:
            print(f"  Progress: {i}/{iterations}")
    
    print(f"\nResults for {url}:")
    print(f"  Mean: {statistics.mean(times):.2f}ms")
    print(f"  Median: {statistics.median(times):.2f}ms")
    print(f"  P95: {sorted(times)[int(len(times)*0.95)]:.2f}ms")
    print(f"  P99: {sorted(times)[int(len(times)*0.99)]:.2f}ms")
    print(f"  Min: {min(times):.2f}ms")
    print(f"  Max: {max(times):.2f}ms")

print("Benchmarking API v1.2 endpoints...\n")
benchmark_endpoint(f"{API_BASE}/status")
benchmark_endpoint(f"{API_BASE}/conversations")
```

**Run:**
```bash
python3 test-app/benchmark.py
```

**Commit:**
```bash
git add test-app/benchmark.py
git commit -m "test: Add performance benchmark script"
```

---

## Testing & Validation

### Pre-Release Checklist

#### API Functionality
- [ ] `GET /api/v1/status` returns correct info
- [ ] `POST /api/v1/conversations` creates conversation
- [ ] `GET /api/v1/conversations` lists conversations
- [ ] `GET /api/v1/conversations/{id}` retrieves specific conversation
- [ ] `POST /api/v1/conversations/{id}/message` processes council query
- [ ] Streaming endpoint works

#### Backward Compatibility
- [ ] Old `/api/conversations` redirects to `/api/v1/conversations`
- [ ] Existing frontend works without changes
- [ ] All v1.1 features functional
- [ ] No breaking changes to data format

#### CORS
- [ ] Cross-origin requests work
- [ ] Preflight OPTIONS requests succeed
- [ ] Configurable origins respected
- [ ] Wildcard (*) works in dev mode

#### Authentication
- [ ] Auth disabled by default (no API_KEYS set)
- [ ] Requests work without X-API-Key header (auth disabled)
- [ ] Requests work with valid X-API-Key (auth enabled)
- [ ] Requests fail with invalid key (auth enabled)
- [ ] Requests fail without key (auth enabled)
- [ ] Status endpoint shows correct auth_required value

#### Versioning
- [ ] All endpoints prefixed with `/api/v1/`
- [ ] Response headers include X-API-Version
- [ ] Response headers include X-Service-Version
- [ ] OpenAPI docs accessible at `/api/v1/docs`

#### Documentation
- [ ] README_API.md complete and accurate
- [ ] All code examples tested and working
- [ ] Main README updated with API section
- [ ] .env.example includes new variables

#### External Integration
- [ ] Test frontend (test-app) works
- [ ] Python example works
- [ ] JavaScript example works
- [ ] curl examples work

#### Performance
- [ ] API overhead < 10ms (benchmark)
- [ ] No performance regression vs v1.1
- [ ] Hot reload still < 2 seconds

---

## Rollback Strategy

### Immediate Rollback

If v1.2 causes critical issues:

```bash
# Stop containers
docker compose down

# Checkout previous version
git checkout v1.1.0  # or commit hash

# Rebuild and restart
docker compose build
docker compose up
```

### Partial Rollback

**Disable auth if causing issues:**
```bash
# Remove from .env
API_KEYS=

# Restart backend
docker compose restart backend
```

**Revert CORS to localhost only:**
```bash
# Update .env
API_CORS_ORIGINS=http://localhost:5173

# Restart backend
docker compose restart backend
```

### Files Changed in v1.2

**New Files (safe to remove):**
- `backend/routers/api_v1.py`
- `backend/middleware/cors.py`
- `backend/middleware/versioning.py`
- `backend/auth.py`
- `README_API.md`
- `test-app/`

**Modified Files (can revert):**
- `backend/main.py`
- `frontend/src/api.js`
- `README.md`
- `.env.example`

---

## Post-Implementation

### Release Tasks

- [ ] Tag release: `git tag v1.2.0`
- [ ] Push tags: `git push --tags`
- [ ] Create GitHub release with notes
- [ ] Update ProductOverview.md
- [ ] Create ReleaseNotes-v1.2.md

### Documentation Tasks

- [ ] Update main README with v1.2 features
- [ ] Ensure README_API.md is complete
- [ ] Add migration guide from v1.1
- [ ] Update CLAUDE.md if present

### Communication

- [ ] Announce v1.2 release
- [ ] Share API documentation link
- [ ] Provide example integrations
- [ ] Collect feedback from first users

### Future Planning

- [ ] Document lessons learned
- [ ] Identify v1.3 candidates
- [ ] Plan for v2.0 (multi-app ecosystem)
- [ ] Consider first external app to build

---

## Appendix

### Quick Reference Commands

```bash
# Development
docker compose up -d
docker compose logs -f backend
docker compose restart backend

# Testing
curl http://localhost:8001/api/v1/status
curl http://localhost:8001/api/v1/conversations

# With auth
curl -H "X-API-Key: key1" http://localhost:8001/api/v1/conversations

# Benchmarking
python3 test-app/benchmark.py

# External test app
cd test-app && python3 -m http.server 8080
```

### Related Documents

- [v1.2 PRD](./PRD-v1.2.md) - Product requirements
- [v1.2 Technical Spec](./TechnicalSpec-v1.2.md) - Architecture details
- [v1.2 Test Plan](./TestPlan-v1.2.md) - Testing strategy
- [Product Overview](../../ProductOverview.md) - System-wide documentation
- [Project Conventions](../../ProjectConventions.md) - Development standards

---

**Implementation Status:** Not Started  
**Last Updated:** December 24, 2025  
**Ready to Begin:** Pending PRD approval ✅

