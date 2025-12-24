"""FastAPI backend for LLM Council."""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Any
import uuid
import json
import asyncio

from . import storage
from . import config
from .council import run_full_council, generate_conversation_title, stage1_collect_responses, stage2_collect_rankings, stage3_synthesize_final, calculate_aggregate_rankings

# Service version for v1.2
SERVICE_VERSION = "1.2.0"
API_VERSION = "v1"

app = FastAPI(
    title="LLM Council API",
    description="""
## LLM Council API - Multi-Perspective AI Insights

The LLM Council API provides a unique multi-model AI deliberation system that generates comprehensive responses through a three-stage process:

### Features
* **Multi-Model Council**: Query multiple leading LLMs simultaneously
* **Ranked Responses**: Models evaluate and rank each other's responses
* **Synthesized Output**: Chairman model creates final comprehensive answer
* **Streaming Support**: Real-time updates as council deliberates
* **Versioned API**: Stable `/api/v1/` endpoints
* **Optional Authentication**: Secure with API keys when needed

### API Versions
* **Current**: v1 (`/api/v1/`)
* **Service Version**: 1.2.0

### Authentication
Authentication is optional and disabled by default. When enabled, include your API key in the `X-API-Key` header.

### External Integration
This API is designed to be called by external applications. CORS is configured for cross-origin requests.

For detailed usage examples, see [README_API.md](../README_API.md)
    """,
    version=SERVICE_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Enable CORS for external applications (FR-1.1)
# Configurable via API_CORS_ORIGINS environment variable
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Middleware to add version headers to all responses (FR-2.2)
@app.middleware("http")
async def add_version_headers(request: Request, call_next):
    """
    Add version headers to all responses.
    
    Implements: FR-2.2 (Version in Response Headers)
    
    Headers:
    - X-API-Version: API version (v1, v2, etc.)
    - X-Service-Version: Service semantic version (1.2.0, etc.)
    """
    response = await call_next(request)
    response.headers["X-API-Version"] = API_VERSION
    response.headers["X-Service-Version"] = SERVICE_VERSION
    return response


# Middleware for optional API key authentication (FR-1.2)
@app.middleware("http")
async def authenticate_api_key(request: Request, call_next):
    """
    Optional API key authentication middleware.
    
    Implements: FR-1.2 (Optional API Authentication)
    
    Behavior:
    - If API_AUTH_ENABLED=false (default): All requests allowed
    - If API_AUTH_ENABLED=true: Validates X-API-Key header
    - Health/status endpoints always accessible
    """
    # Skip auth for health/status endpoints
    if request.url.path in ["/", "/health", "/api/v1/status"]:
        return await call_next(request)
    
    # If auth is disabled, allow all requests
    if not config.API_AUTH_ENABLED:
        return await call_next(request)
    
    # Auth is enabled - validate API key
    api_key = request.headers.get("X-API-Key")
    
    if not api_key:
        return JSONResponse(
            status_code=401,
            content={"detail": "API key required. Include X-API-Key header."}
        )
    
    if api_key not in config.API_KEYS:
        return JSONResponse(
            status_code=401,
            content={"detail": "Invalid API key"}
        )
    
    # Valid API key - proceed
    return await call_next(request)


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


@app.get("/")
async def root():
    """Root endpoint."""
    return {"status": "ok", "service": "LLM Council API"}


@app.get("/health")
async def health_check():
    """
    Health check endpoint for Docker container orchestration.
    
    Implements: FR-1.3 (Backend Health Check)
    
    Returns service status for Docker health checks and monitoring.
    """
    return {"status": "healthy", "service": "LLM Council API"}


@app.get("/api/v1/status")
async def get_service_status():
    """
    Get service metadata and health status.
    
    Implements: FR-1.3 (Service Metadata Endpoint)
    
    Returns comprehensive service information useful for:
    - Health monitoring
    - API discovery
    - Feature detection
    - Configuration inspection
    
    **Example Response:**
    ```json
    {
      "service": "LLM Council API",
      "version": "1.2.0",
      "api_version": "v1",
      "status": "healthy",
      "models": {
        "council": ["openai/gpt-5.1", "google/gemini-3-pro-preview", ...],
        "chairman": "google/gemini-3-pro-preview"
      },
      "features": {
        "auth_required": false,
        "streaming": true,
        "versioned_api": true
      }
    }
    ```
    """
    return {
        "service": "LLM Council API",
        "version": SERVICE_VERSION,
        "api_version": API_VERSION,
        "status": "healthy",
        "models": {
            "council": config.COUNCIL_MODELS,
            "chairman": config.CHAIRMAN_MODEL
        },
        "features": {
            "auth_required": config.API_AUTH_ENABLED,
            "streaming": True,
            "versioned_api": True
        }
    }


# ==================== API v1 Routes ====================
# All new endpoints use /api/v1/ prefix per FR-2.1

@app.get("/api/v1/conversations", response_model=List[ConversationMetadata])
async def list_conversations_v1():
    """List all conversations (metadata only) - API v1."""
    return storage.list_conversations()


@app.post("/api/v1/conversations", response_model=Conversation)
async def create_conversation_v1(request: CreateConversationRequest):
    """Create a new conversation - API v1."""
    conversation_id = str(uuid.uuid4())
    conversation = storage.create_conversation(conversation_id)
    return conversation


@app.get("/api/v1/conversations/{conversation_id}", response_model=Conversation)
async def get_conversation_v1(conversation_id: str):
    """Get a specific conversation with all its messages - API v1."""
    conversation = storage.get_conversation(conversation_id)
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation


@app.post("/api/v1/conversations/{conversation_id}/message")
async def send_message_v1(conversation_id: str, request: SendMessageRequest):
    """
    Send a message and run the 3-stage council process - API v1.
    Returns the complete response with all stages.
    
    Implements: FR-2.1 (Version Prefix)
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


@app.post("/api/v1/conversations/{conversation_id}/message/stream")
async def send_message_stream_v1(conversation_id: str, request: SendMessageRequest):
    """
    Send a message and stream the 3-stage council process - API v1.
    Returns Server-Sent Events as each stage completes.
    
    Implements: FR-2.1 (Version Prefix)
    """
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


# ==================== Legacy Route Aliases (v1.1 Compatibility) ====================
# Maintain backward compatibility per FR-2.1 and NFR-2.1
# These routes alias to the v1 endpoints

@app.get("/api/conversations", response_model=List[ConversationMetadata])
async def list_conversations():
    """List all conversations (metadata only) - Legacy alias."""
    return await list_conversations_v1()


@app.post("/api/conversations", response_model=Conversation)
async def create_conversation(request: CreateConversationRequest):
    """Create a new conversation - Legacy alias."""
    return await create_conversation_v1(request)


@app.get("/api/conversations/{conversation_id}", response_model=Conversation)
async def get_conversation(conversation_id: str):
    """Get a specific conversation with all its messages - Legacy alias."""
    return await get_conversation_v1(conversation_id)


@app.post("/api/conversations/{conversation_id}/message")
async def send_message(conversation_id: str, request: SendMessageRequest):
    """Send a message and run the 3-stage council process - Legacy alias."""
    return await send_message_v1(conversation_id, request)


@app.post("/api/conversations/{conversation_id}/message/stream")
async def send_message_stream(conversation_id: str, request: SendMessageRequest):
    """Send a message and stream the 3-stage council process - Legacy alias."""
    return await send_message_stream_v1(conversation_id, request)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
