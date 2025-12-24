# LLM Council API Documentation

**API Version:** v1  
**Service Version:** 1.2.0  
**Base URL:** `http://localhost:8001`

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Authentication](#authentication)
3. [API Endpoints](#api-endpoints)
4. [Request/Response Formats](#requestresponse-formats)
5. [Error Handling](#error-handling)
6. [Code Examples](#code-examples)
7. [Rate Limits](#rate-limits)
8. [Versioning](#versioning)

---

## Quick Start

### Python

```python
import requests

# Create a conversation
response = requests.post("http://localhost:8001/api/v1/conversations", json={})
conversation_id = response.json()["id"]

# Send a message
response = requests.post(
    f"http://localhost:8001/api/v1/conversations/{conversation_id}/message",
    json={"content": "What is quantum computing?"}
)

result = response.json()
print(result["stage3"]["response"])
```

### JavaScript

```javascript
// Create a conversation
const createResp = await fetch("http://localhost:8001/api/v1/conversations", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({})
});
const { id: conversationId } = await createResp.json();

// Send a message
const msgResp = await fetch(
  `http://localhost:8001/api/v1/conversations/${conversationId}/message`,
  {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ content: "What is quantum computing?" })
  }
);

const result = await msgResp.json();
console.log(result.stage3.response);
```

### curl

```bash
# Create a conversation
CONV_ID=$(curl -s -X POST http://localhost:8001/api/v1/conversations \
  -H "Content-Type: application/json" \
  -d '{}' | jq -r '.id')

# Send a message
curl -X POST http://localhost:8001/api/v1/conversations/$CONV_ID/message \
  -H "Content-Type: application/json" \
  -d '{"content": "What is quantum computing?"}' | jq '.stage3.response'
```

---

## Authentication

### Overview

Authentication is **optional** and disabled by default. When enabled, include your API key in the `X-API-Key` header.

### Enabling Authentication

Set these environment variables:

```bash
API_AUTH_ENABLED=true
API_KEYS=your-key-1,your-key-2,your-key-3
```

### Using API Keys

**With Authentication:**

```python
headers = {
    "Content-Type": "application/json",
    "X-API-Key": "your-key-here"
}
response = requests.get("http://localhost:8001/api/v1/conversations", headers=headers)
```

**Without Authentication (default):**

```python
headers = {"Content-Type": "application/json"}
response = requests.get("http://localhost:8001/api/v1/conversations", headers=headers)
```

### Authentication Errors

**401 Unauthorized** - Invalid or missing API key when auth is enabled:

```json
{
  "detail": "Invalid API key"
}
```

---

## API Endpoints

### Service Metadata

#### `GET /api/v1/status`

Get service metadata, health status, and feature information.

**Response:**

```json
{
  "service": "LLM Council API",
  "version": "1.2.0",
  "api_version": "v1",
  "status": "healthy",
  "models": {
    "council": ["openai/gpt-5.1", "google/gemini-3-pro-preview", "anthropic/claude-sonnet-4.5", "x-ai/grok-4"],
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

### Conversations

#### `GET /api/v1/conversations`

List all conversations (metadata only).

**Response:**

```json
[
  {
    "id": "abc-123",
    "created_at": "2025-12-24T10:00:00Z",
    "title": "Quantum Computing Discussion",
    "message_count": 5
  }
]
```

#### `POST /api/v1/conversations`

Create a new conversation.

**Request Body:**

```json
{}
```

**Response:**

```json
{
  "id": "abc-123",
  "created_at": "2025-12-24T10:00:00Z",
  "title": "New Conversation",
  "messages": []
}
```

#### `GET /api/v1/conversations/{conversation_id}`

Get a specific conversation with all messages.

**Response:**

```json
{
  "id": "abc-123",
  "created_at": "2025-12-24T10:00:00Z",
  "title": "Quantum Computing Discussion",
  "messages": [
    {
      "role": "user",
      "content": "What is quantum computing?",
      "timestamp": "2025-12-24T10:00:00Z"
    },
    {
      "role": "assistant",
      "stage1": [...],
      "stage2": [...],
      "stage3": {...},
      "timestamp": "2025-12-24T10:00:05Z"
    }
  ]
}
```

---

### Messages

#### `POST /api/v1/conversations/{conversation_id}/message`

Send a message and run the 3-stage council process.

**Request Body:**

```json
{
  "content": "What is quantum computing?"
}
```

**Response:**

```json
{
  "stage1": [
    {
      "model": "openai/gpt-5.1",
      "response": "Quantum computing uses quantum mechanics..."
    },
    {
      "model": "google/gemini-3-pro-preview",
      "response": "Quantum computers leverage superposition..."
    }
  ],
  "stage2": [
    {
      "model": "openai/gpt-5.1",
      "rankings": [
        {"rank": 1, "model_label": "B", "reasoning": "..."},
        {"rank": 2, "model_label": "A", "reasoning": "..."}
      ]
    }
  ],
  "stage3": {
    "response": "Based on the council's deliberation, quantum computing...",
    "model": "google/gemini-3-pro-preview"
  },
  "metadata": {
    "aggregate_rankings": {...}
  }
}
```

#### `POST /api/v1/conversations/{conversation_id}/message/stream`

Send a message and receive streaming updates (Server-Sent Events).

**Request Body:**

```json
{
  "content": "What is quantum computing?"
}
```

**Response Stream (SSE):**

```
data: {"type": "stage1_start"}

data: {"type": "stage1_complete", "data": [...]}

data: {"type": "stage2_start"}

data: {"type": "stage2_complete", "data": [...], "metadata": {...}}

data: {"type": "stage3_start"}

data: {"type": "stage3_complete", "data": {...}}

data: {"type": "complete"}
```

---

## Request/Response Formats

### Common Headers

**Request Headers:**

```
Content-Type: application/json
X-API-Key: your-key-here  (optional, when auth enabled)
```

**Response Headers:**

```
Content-Type: application/json
X-API-Version: v1
X-Service-Version: 1.2.0
Access-Control-Allow-Origin: *  (or configured origins)
```

### Timestamps

All timestamps use ISO 8601 format:

```
2025-12-24T10:00:00.123456Z
```

### IDs

All conversation IDs are UUIDs:

```
abc-123-def-456-ghi-789
```

---

## Error Handling

### Standard Error Format

```json
{
  "detail": "Error message"
}
```

### HTTP Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request succeeded |
| 401 | Unauthorized | Invalid or missing API key |
| 404 | Not Found | Conversation not found |
| 422 | Unprocessable Entity | Invalid request body |
| 500 | Internal Server Error | Server error |

### Example Error Handling

**Python:**

```python
try:
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    result = response.json()
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 401:
        print("Invalid API key")
    elif e.response.status_code == 404:
        print("Conversation not found")
    else:
        print(f"Error: {e.response.json()['detail']}")
```

**JavaScript:**

```javascript
try {
  const response = await fetch(url, options);
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail);
  }
  const result = await response.json();
} catch (error) {
  console.error("API Error:", error.message);
}
```

---

## Code Examples

### Complete Workflow (Python)

```python
import requests

BASE_URL = "http://localhost:8001/api/v1"
HEADERS = {
    "Content-Type": "application/json",
    # "X-API-Key": "your-key-here"  # Uncomment if auth enabled
}

# 1. Check service status
status = requests.get(f"{BASE_URL}/status").json()
print(f"Service: {status['service']} v{status['version']}")
print(f"Auth required: {status['features']['auth_required']}")

# 2. Create a conversation
conv_resp = requests.post(f"{BASE_URL}/conversations", json={}, headers=HEADERS)
conversation_id = conv_resp.json()["id"]
print(f"Created conversation: {conversation_id}")

# 3. Send a message
msg_resp = requests.post(
    f"{BASE_URL}/conversations/{conversation_id}/message",
    json={"content": "Explain blockchain in simple terms"},
    headers=HEADERS
)
result = msg_resp.json()

# 4. Process the response
print("\n=== Stage 1: Council Responses ===")
for resp in result["stage1"]:
    print(f"\n{resp['model']}:")
    print(resp["response"][:200] + "...")

print("\n=== Stage 3: Final Synthesis ===")
print(result["stage3"]["response"])

# 5. Get conversation history
history = requests.get(
    f"{BASE_URL}/conversations/{conversation_id}",
    headers=HEADERS
).json()
print(f"\nConversation has {len(history['messages'])} messages")
```

### Streaming Example (JavaScript)

```javascript
async function streamCouncilResponse(conversationId, message) {
  const response = await fetch(
    `http://localhost:8001/api/v1/conversations/${conversationId}/message/stream`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        // "X-API-Key": "your-key-here"  // Uncomment if auth enabled
      },
      body: JSON.stringify({ content: message })
    }
  );

  const reader = response.body.getReader();
  const decoder = new TextDecoder();

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    const chunk = decoder.decode(value);
    const lines = chunk.split('\n');

    for (const line of lines) {
      if (line.startsWith('data: ')) {
        const data = line.slice(6);
        try {
          const event = JSON.parse(data);
          
          switch (event.type) {
            case 'stage1_start':
              console.log("Stage 1: Collecting council responses...");
              break;
            case 'stage1_complete':
              console.log(`Stage 1 complete: ${event.data.length} responses`);
              break;
            case 'stage2_start':
              console.log("Stage 2: Ranking responses...");
              break;
            case 'stage2_complete':
              console.log("Stage 2 complete: Rankings received");
              break;
            case 'stage3_start':
              console.log("Stage 3: Synthesizing final answer...");
              break;
            case 'stage3_complete':
              console.log("Stage 3 complete!");
              console.log("\nFinal Answer:");
              console.log(event.data.response);
              break;
            case 'complete':
              console.log("\nCouncil deliberation complete!");
              break;
          }
        } catch (e) {
          console.error('Failed to parse event:', e);
        }
      }
    }
  }
}

// Usage
const convResp = await fetch("http://localhost:8001/api/v1/conversations", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({})
});
const { id } = await convResp.json();

await streamCouncilResponse(id, "What are the implications of AI?");
```

---

## Rate Limits

**Current Status:** No rate limiting (v1.2)

Rate limiting will be added in v1.3 when multiple external apps exist.

---

## Versioning

### API Version Strategy

- All routes are prefixed with `/api/v1/`
- Breaking changes go to `/api/v2/`
- Non-breaking changes added to current version
- Deprecated endpoints announced 6 months in advance

### Version Headers

Every response includes:

```
X-API-Version: v1
X-Service-Version: 1.2.0
```

### Legacy Routes

Old `/api/` routes (v1.1) are aliased for backward compatibility:

- `/api/conversations` → `/api/v1/conversations`

**⚠️ Deprecation Notice:** Legacy routes will be removed in v1.3 (target: Q1 2026)

### Migration Guide

**From v1.1 to v1.2:**

1. Update all `/api/` routes to `/api/v1/`
2. No other changes required (backward compatible)

```diff
- fetch("http://localhost:8001/api/conversations")
+ fetch("http://localhost:8001/api/v1/conversations")
```

---

## Support & Resources

- **OpenAPI Documentation:** http://localhost:8001/docs
- **ReDoc Documentation:** http://localhost:8001/redoc
- **OpenAPI JSON Schema:** http://localhost:8001/openapi.json
- **GitHub Issues:** [Report bugs or request features]
- **Main README:** [Project overview and setup]

---

## Changelog

### v1.2.0 (2025-12-24)

**Added:**
- API versioning (`/api/v1/` prefix)
- Version headers in responses
- CORS configuration for external apps
- `/api/v1/status` metadata endpoint
- Optional API key authentication
- Enhanced OpenAPI documentation

**Changed:**
- All routes now use `/api/v1/` prefix
- Legacy routes aliased for backward compatibility

**No Breaking Changes:** All v1.1 functionality maintained

---

**Last Updated:** December 24, 2025  
**API Version:** v1  
**Service Version:** 1.2.0

