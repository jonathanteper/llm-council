# Release Notes: LLM Council v1.0.0

**Release Date:** October 15, 2025  
**Version:** 1.0.0  
**Status:** Shipped  
**Type:** Initial Release

---

## Overview

LLM Council v1.0.0 is the initial release of a local web application that enables querying multiple Large Language Models through a three-stage deliberation process. This release establishes the core council functionality and provides a working foundation for future enhancements.

---

## What's New

### 🎉 Core Features

#### Three-Stage Council Process
- **Stage 1:** Query sent to all configured LLMs, individual responses displayed in tabs
- **Stage 2:** Anonymized cross-review where each LLM ranks others' responses
- **Stage 3:** Chairman synthesis providing final answer incorporating all perspectives

#### Conversation Management
- Create new conversations with unique identifiers
- View conversation history in sidebar
- Continue existing conversations with follow-up queries
- Persistent storage of all conversations as JSON files

#### Council Configuration
- Default council: GPT-5.1, Gemini 3 Pro, Claude Sonnet 4.5, Grok 4
- Default chairman: Gemini 3 Pro
- Configurable via `backend/config.py`

#### User Interface
- Clean chat interface similar to ChatGPT
- Tab-based navigation between stages
- Markdown rendering with syntax highlighting
- Conversation sidebar for easy navigation

---

## Requirements Implemented

### Functional Requirements

✅ **[v1.0-FR-1]** Three-stage council processing  
✅ **[v1.0-FR-1.1]** Stage 1: Individual responses  
✅ **[v1.0-FR-1.2]** Stage 2: Cross-review  
✅ **[v1.0-FR-1.3]** Stage 3: Chairman synthesis  
✅ **[v1.0-FR-2]** Conversation management  
✅ **[v1.0-FR-2.1]** Create conversations  
✅ **[v1.0-FR-2.2]** View history  
✅ **[v1.0-FR-2.3]** Continue conversations  
✅ **[v1.0-FR-3]** Council configuration  
✅ **[v1.0-FR-3.1]** Configure council members  
✅ **[v1.0-FR-3.2]** Configure chairman  
✅ **[v1.0-FR-4]** User interface  
✅ **[v1.0-FR-4.1]** Query input  
✅ **[v1.0-FR-4.2]** Stage navigation  
✅ **[v1.0-FR-4.3]** Markdown rendering  

### Non-Functional Requirements

✅ **[v1.0-NFR-1.1]** Response time < 30 seconds (Stage 1 start)  
✅ **[v1.0-NFR-2.1]** API error handling  
✅ **[v1.0-NFR-2.2]** Data persistence  
✅ **[v1.0-NFR-3.1]** Simple setup (just API key required)  
✅ **[v1.0-NFR-3.2]** Local operation  
✅ **[v1.0-NFR-4.1]** Simple, readable code  

---

## Technical Details

### Technology Stack

**Backend:**
- FastAPI 0.115+ (Python 3.10+)
- Uvicorn ASGI server
- httpx for async HTTP
- python-dotenv for configuration
- uv for package management

**Frontend:**
- React 19.2
- Vite 7.2 build tool
- react-markdown for rendering
- Modern ES6+ JavaScript

**Storage:**
- JSON file-based persistence
- Location: `data/conversations/`

**External Services:**
- OpenRouter API for LLM access

### Architecture

```
User Browser
    ↓
React Frontend (localhost:5173)
    ↓
FastAPI Backend (localhost:8001)
    ↓
OpenRouter API
    ↓
Multiple LLMs (GPT, Gemini, Claude, Grok)
```

---

## Installation & Setup

### Prerequisites
- Python 3.10 or higher
- Node.js 20 LTS
- OpenRouter API key with credits

### Installation Steps

1. **Install Backend Dependencies:**
   ```bash
   uv sync
   ```

2. **Install Frontend Dependencies:**
   ```bash
   cd frontend
   npm install
   cd ..
   ```

3. **Configure API Key:**
   Create `.env` file:
   ```bash
   OPENROUTER_API_KEY=sk-or-v1-your-key-here
   ```

4. **Start Application:**
   ```bash
   ./start.sh
   ```
   
   Or manually:
   ```bash
   # Terminal 1:
   uv run python -m backend.main
   
   # Terminal 2:
   cd frontend && npm run dev
   ```

5. **Open Browser:**
   Navigate to http://localhost:5173

---

## Known Issues & Limitations

### Limitations by Design

❌ **No User Authentication:** Single-user local application  
❌ **No Response Caching:** Each query costs API credits  
❌ **No Conversation Search:** Manual browsing only  
❌ **No Export Function:** Cannot export to PDF/Markdown  
❌ **Local Only:** Not designed for cloud deployment  
❌ **No Mobile Support:** Desktop browsers only  

### Known Bugs

None identified in initial release.

---

## Breaking Changes

N/A - This is the initial release.

---

## Migration Guide

N/A - This is the initial release.

---

## Dependencies

### Python Dependencies
```
fastapi>=0.115.0
uvicorn[standard]>=0.32.0
python-dotenv>=1.0.0
httpx>=0.27.0
pydantic>=2.9.0
```

### JavaScript Dependencies
```
react@19.2.0
react-dom@19.2.0
react-markdown@10.1.0
vite@7.2.4
```

---

## Performance

### Typical Response Times
- Stage 1 (4 LLMs): 15-30 seconds
- Stage 2 (4 reviews): 20-40 seconds
- Stage 3 (synthesis): 10-20 seconds
- **Total:** ~1-2 minutes per query

*Note: Times depend on LLM API response times and query complexity*

---

## Security

### Security Measures
✅ API key stored in `.env` file (not in code)  
✅ `.env` file in `.gitignore`  
✅ All communication over HTTPS (to OpenRouter)  
✅ No user data sent to external services (except queries to LLMs)  
✅ Local data storage only  

### Security Limitations
⚠️ No encryption of local JSON files  
⚠️ No API key encryption at rest  
⚠️ Suitable for local development only  

---

## Credits

**Original Concept:** Inspired by desire to compare LLMs side-by-side while reading books with AI assistance

**Development Philosophy:** "Vibe coded" - Simple, functional, easily modifiable

**Open Source:** MIT License (assumed)

---

## Next Steps

### Planned for v1.1
- Docker containerization for simplified setup
- Eliminate Python/Node.js installation requirement
- Maintain hot reload for development

### Future Ideas
- User authentication (v2.0)
- Cloud deployment support
- Response caching
- Conversation search
- Export functionality

---

## Feedback & Support

**This Project:** Community-driven, no official support

**Issues:** Users encouraged to fork and modify as needed

**Philosophy:** "Code is ephemeral now and libraries are over, ask your LLM to change it in whatever way you like."

---

## Related Documents

- [PRD v1.0](./PRD-v1.0.md) - Full requirements document
- [Product Overview](../../ProductOverview.md) - System-wide documentation
- [Main README](../../../README.md) - User guide

---

**Release Status:** ✅ Stable  
**Released By:** Development Team  
**Release Date:** October 15, 2025

