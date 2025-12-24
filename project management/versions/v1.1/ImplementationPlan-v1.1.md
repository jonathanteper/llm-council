# Implementation Plan: LLM Council v1.1 - Containerization

**Version:** 1.1  
**Date:** December 24, 2025  
**Status:** Ready for Implementation  
**Estimated Duration:** 1-2 weeks

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Phase 1: Backend Dockerization](#phase-1-backend-dockerization)
4. [Phase 2: Frontend Dockerization](#phase-2-frontend-dockerization)
5. [Phase 3: Docker Compose Integration](#phase-3-docker-compose-integration)
6. [Phase 4: Developer Experience](#phase-4-developer-experience)
7. [Testing & Validation](#testing--validation)
8. [Rollback Strategy](#rollback-strategy)
9. [Post-Implementation](#post-implementation)

---

## Overview

This document provides a step-by-step guide for implementing containerization of the LLM Council application. The implementation is divided into four phases, each building on the previous one.

### Implementation Approach

- **Incremental:** Build and test each component before moving to the next
- **Non-Breaking:** Keep existing native development workflow intact
- **Validated:** Test after each phase to catch issues early
- **Documented:** Update documentation as we go

### Success Criteria

By the end of implementation:
- ✅ Both containers build successfully
- ✅ Application runs with `docker compose up`
- ✅ Hot reload works for both backend and frontend
- ✅ All existing functionality preserved
- ✅ Documentation updated with Docker instructions

---

## Prerequisites

### System Requirements

**Required Software:**
- [ ] **OrbStack** installed (https://orbstack.dev)
  - Alternative: Docker Desktop (will work but not optimized)
- [ ] **Git** for version control
- [ ] **Text editor** (VSCode, Cursor, etc.)

**Verify Installation:**
```bash
# Check OrbStack/Docker
docker --version
# Expected: Docker version 24.x or higher

docker compose version
# Expected: Docker Compose version v2.x or higher

# Check OrbStack is running
docker ps
# Should not error
```

### Project Requirements

**Existing Files:**
- [ ] `.env` file with valid `OPENROUTER_API_KEY`
- [ ] Working native setup (can run with `./start.sh`)
- [ ] Conversations in `data/conversations/` (optional, for testing persistence)

**Verify Current Setup:**
```bash
# Check .env exists
ls -la .env

# Check backend can run
uv run python -m backend.main
# Should start without errors (Ctrl+C to stop)

# Check frontend can run
cd frontend && npm run dev
# Should start without errors (Ctrl+C to stop)
```

### Backup (Recommended)

```bash
# Create backup of current state
git status  # Ensure no uncommitted changes
git add -A
git commit -m "Pre-containerization checkpoint"

# Or create a branch
git checkout -b containerization
```

---

## Phase 1: Backend Dockerization

**Goal:** Create a working Docker container for the FastAPI backend.

**Duration:** 2-3 hours

### Step 1.1: Create Backend Dockerfile

Create `backend.Dockerfile` in project root:

```dockerfile
# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv package manager
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:${PATH}"

# Copy dependency files
COPY pyproject.toml uv.lock* ./

# Install Python dependencies
RUN uv sync --frozen

# Copy backend source
COPY backend/ ./backend/

# Expose backend port
EXPOSE 8001

# Ensure Python output is sent straight to terminal
ENV PYTHONUNBUFFERED=1

# Run the backend server
CMD ["uv", "run", "python", "-m", "backend.main"]
```

**Key Design Decisions:**
- Use `slim` variant (not `alpine`) for better compatibility with uv
- Install curl for health checks
- Copy dependencies before source code (better layer caching)
- Use `uv.lock*` glob to handle missing lockfile gracefully

### Step 1.2: Create Backend .dockerignore

Create `.dockerignore` in project root:

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/

# IDEs
.vscode/
.idea/
*.swp
*.swo
.DS_Store

# Git
.git/
.gitignore

# Data (will be mounted as volume)
data/

# Frontend (not needed in backend image)
frontend/
node_modules/

# Documentation
*.md
docs/

# Environment
.env
.env.*

# Misc
*.log
.cache/
```

### Step 1.3: Test Backend Container Build

```bash
# Build the backend image
docker build -f backend.Dockerfile -t llm-council-backend:test .

# Expected output: Successfully built and tagged
```

**Troubleshooting:**
- If build fails at uv install, check internet connection
- If Python package errors, verify `pyproject.toml` is valid
- Use `docker build --no-cache` to force clean build

### Step 1.4: Test Backend Container Run

```bash
# Run backend container with volumes
docker run -d \
  --name backend-test \
  -p 8001:8001 \
  -v "$(pwd)/backend:/app/backend" \
  -v "$(pwd)/data:/app/data" \
  -v "$(pwd)/.env:/app/.env:ro" \
  llm-council-backend:test

# Check logs
docker logs backend-test

# Expected: Backend starts on port 8001
```

**Verify Backend:**
```bash
# Health check
curl http://localhost:8001/health
# Expected: 200 OK or health status

# Check .env loaded
docker logs backend-test | grep "API key loaded"
# Expected: Should show key prefix
```

**Test Hot Reload:**
```bash
# Make a small change to backend/config.py (add a comment)
# Check logs for reload message
docker logs -f backend-test
# Expected: "Detected file change, reloading..."
```

**Cleanup Test:**
```bash
docker stop backend-test
docker rm backend-test
```

### Step 1.5: Add Backend Health Endpoint

If not already present, add health endpoint to `backend/main.py`:

```python
@app.get("/health")
async def health_check():
    """Health check endpoint for Docker."""
    return {
        "status": "healthy",
        "service": "llm-council-backend",
        "timestamp": datetime.now().isoformat()
    }
```

**Test:**
```bash
# Start backend natively
uv run python -m backend.main

# In another terminal
curl http://localhost:8001/health
```

---

## Phase 2: Frontend Dockerization

**Goal:** Create a working Docker container for the Vite/React frontend.

**Duration:** 2-3 hours

### Step 2.1: Create Frontend Dockerfile

Create `frontend/frontend.Dockerfile`:

```dockerfile
# Use Node 20 Alpine for smaller image
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Install wget for health checks
RUN apk add --no-cache wget

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY . .

# Expose Vite dev server port
EXPOSE 5173

# Run Vite dev server
# --host 0.0.0.0 allows external connections
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
```

**Key Design Decisions:**
- Use Alpine variant for smaller size
- `npm ci` instead of `npm install` (faster, more reliable)
- `--host 0.0.0.0` critical for container networking
- Copy all files (source will be volume mounted in compose)

### Step 2.2: Create Frontend .dockerignore

Create `frontend/.dockerignore`:

```
# Dependencies
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
package-lock.json

# Production build
dist/
build/

# Environment
.env
.env.*

# IDEs
.vscode/
.idea/
*.swp
*.swo
.DS_Store

# Git
.git/
.gitignore

# Testing
coverage/

# Misc
*.log
.cache/
```

### Step 2.3: Update Vite Configuration

Edit `frontend/vite.config.js` to support containerization:

```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0', // Listen on all interfaces
    port: 5173,
    watch: {
      usePolling: false, // OrbStack handles file watching well
      // If hot reload doesn't work, uncomment:
      // usePolling: true,
      // interval: 1000,
    },
    hmr: {
      host: 'localhost', // HMR websocket connects via localhost
      port: 5173,
    }
  }
})
```

**Commit this change:**
```bash
git add frontend/vite.config.js
git commit -m "Configure Vite for container networking"
```

### Step 2.4: Test Frontend Container Build

```bash
# Build the frontend image
docker build -f frontend/frontend.Dockerfile -t llm-council-frontend:test ./frontend

# Expected output: Successfully built and tagged
```

### Step 2.5: Test Frontend Container Run

```bash
# Ensure backend is running (natively or in container)
# Run frontend container with volumes
docker run -d \
  --name frontend-test \
  -p 5173:5173 \
  -v "$(pwd)/frontend:/app" \
  -v /app/node_modules \
  -e VITE_API_URL=http://localhost:8001 \
  llm-council-frontend:test

# Check logs
docker logs -f frontend-test

# Expected: "Local: http://localhost:5173/"
```

**Verify Frontend:**
```bash
# Open in browser
open http://localhost:5173

# Check HMR (Hot Module Replacement)
# Edit frontend/src/App.jsx (change some text)
# Browser should update without refresh
```

**Cleanup Test:**
```bash
docker stop frontend-test
docker rm frontend-test
```

---

## Phase 3: Docker Compose Integration

**Goal:** Orchestrate both containers with Docker Compose.

**Duration:** 2-3 hours

### Step 3.1: Create docker-compose.yml

Create `docker-compose.yml` in project root:

```yaml
version: '3.9'

services:
  backend:
    build:
      context: .
      dockerfile: backend.Dockerfile
    container_name: llm-council-backend
    ports:
      - "8001:8001"
    volumes:
      - ./backend:/app/backend
      - ./data:/app/data
      - ./.env:/app/.env:ro
    environment:
      - PYTHONUNBUFFERED=1
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8001/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    restart: unless-stopped
    networks:
      - llm-council-network

  frontend:
    build:
      context: ./frontend
      dockerfile: frontend.Dockerfile
    container_name: llm-council-frontend
    ports:
      - "5173:5173"
    volumes:
      - ./frontend:/app
      - /app/node_modules
    environment:
      - VITE_API_URL=http://localhost:8001
      - NODE_ENV=development
    depends_on:
      backend:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "wget", "--no-verbose", "--tries=1", "--spider", "http://localhost:5173"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s
    restart: unless-stopped
    networks:
      - llm-council-network

networks:
  llm-council-network:
    driver: bridge
```

### Step 3.2: Test Docker Compose Build

```bash
# Stop any running containers
docker compose down

# Build both services
docker compose build

# Expected: Both images build successfully
```

**Troubleshooting:**
- If builds fail, check individual Dockerfiles from Phase 1 & 2
- Use `docker compose build --no-cache backend` to rebuild specific service

### Step 3.3: Test Docker Compose Up

```bash
# Start all services
docker compose up

# Expected output:
# - Backend starts and becomes healthy
# - Frontend waits for backend health check
# - Frontend starts after backend is healthy
# - Both services log to console
```

**What to Look For:**
```
✓ Backend log: "Uvicorn running on http://0.0.0.0:8001"
✓ Backend log: "API key loaded: sk-or-v1..."
✓ Frontend log: "Local: http://localhost:5173/"
✓ No error messages
```

### Step 3.4: Test Application Functionality

Open browser to http://localhost:5173 and test:

**Basic Functionality:**
- [ ] Page loads without errors
- [ ] UI renders correctly
- [ ] Can start a new conversation
- [ ] Can submit a query to the council
- [ ] Responses appear from multiple LLMs
- [ ] Can view stage 2 (review) and stage 3 (final)
- [ ] Can navigate between conversations in sidebar

**Hot Reload:**
- [ ] Edit `backend/config.py` → backend reloads
- [ ] Edit `frontend/src/App.jsx` → browser updates without refresh
- [ ] No container restarts required

**Data Persistence:**
- [ ] Create a conversation
- [ ] Stop containers: `Ctrl+C`
- [ ] Restart: `docker compose up`
- [ ] Conversation still appears in sidebar

### Step 3.5: Test Background Mode

```bash
# Stop foreground mode
Ctrl+C

# Start in background
docker compose up -d

# Check status
docker compose ps
# Expected: Both services "running" and "healthy"

# Follow logs
docker compose logs -f

# Stop background mode
docker compose down
```

---

## Phase 4: Developer Experience

**Goal:** Polish the developer experience with documentation and helpers.

**Duration:** 2-3 hours

### Step 4.1: Create docker-start.sh Helper Script

Create `docker-start.sh` in project root:

```bash
#!/bin/bash

# LLM Council - Docker Start Script

echo "Starting LLM Council with Docker..."
echo ""

# Check if OrbStack/Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker is not running"
    echo "Please start OrbStack or Docker Desktop and try again"
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found"
    echo "Please create .env file with your OPENROUTER_API_KEY"
    echo "Example: OPENROUTER_API_KEY=sk-or-v1-your-key-here"
    exit 1
fi

# Check if API key is set
if grep -q "your-api-key-here" .env 2>/dev/null; then
    echo "⚠️  Warning: .env file contains placeholder API key"
    echo "Please update .env with your real OpenRouter API key"
    exit 1
fi

echo "✓ Docker is running"
echo "✓ .env file found"
echo ""

# Build containers if needed
echo "Building containers (if needed)..."
docker compose build

echo ""
echo "Starting services..."
docker compose up

# Cleanup on exit
trap "docker compose down" EXIT
```

Make it executable:
```bash
chmod +x docker-start.sh
```

### Step 4.2: Update Main README

Add Docker instructions to `README.md`. Insert this section after the existing "Running the Application" section:

```markdown
## Running with Docker (Recommended)

Docker provides an isolated environment and eliminates dependency management.

### Prerequisites

1. Install [OrbStack](https://orbstack.dev) (recommended for macOS) or [Docker Desktop](https://www.docker.com/products/docker-desktop)
2. Create `.env` file (see step 2 in Setup above)

### Start with Docker

**Option 1: Using Docker Compose**
```bash
docker compose up
```

**Option 2: Using the helper script**
```bash
./docker-start.sh
```

**Option 3: Background mode**
```bash
docker compose up -d           # Start in background
docker compose logs -f         # View logs
docker compose down           # Stop services
```

The application will be available at:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8001

### Docker Development Notes

- **Hot Reload**: Code changes are automatically detected and applied
- **Data Persistence**: Conversations are saved to `data/conversations/` on your host machine
- **Rebuilding**: After changing dependencies, run `docker compose build`
- **Cleanup**: Use `docker compose down` to stop and remove containers

### Native vs Docker

Both workflows are supported:
- **Native** (`./start.sh`): Faster startup, requires Python + Node.js installed
- **Docker** (`docker compose up`): No local dependencies, consistent environment
```

### Step 4.3: Create Troubleshooting Guide

Create `project management/Docker-Troubleshooting.md`:

```markdown
# Docker Troubleshooting Guide

## Common Issues

### Port Already in Use

**Problem:** Error message `bind: address already in use`

**Solution:**
```bash
# Find what's using the ports
lsof -i :8001
lsof -i :5173

# Kill the process or stop native version
pkill -f "uvicorn"
pkill -f "vite"

# Then try again
docker compose up
```

### Hot Reload Not Working

**Problem:** File changes don't trigger reload

**Solutions:**

1. **Check volume mounts:**
```bash
docker compose exec backend ls -la /app/backend
docker compose exec frontend ls -la /app/src
```

2. **Try polling mode** (edit `frontend/vite.config.js`):
```javascript
watch: {
  usePolling: true,
  interval: 1000,
}
```

3. **Restart containers:**
```bash
docker compose restart
```

### Backend Can't Load API Key

**Problem:** Backend logs show "API key not set"

**Solution:**
```bash
# Verify .env file exists
cat .env

# Check it's mounted correctly
docker compose exec backend cat /app/.env

# Restart backend
docker compose restart backend
```

### Frontend Can't Connect to Backend

**Problem:** Network errors in browser console

**Solutions:**

1. **Check backend is healthy:**
```bash
curl http://localhost:8001/health
```

2. **Check backend logs:**
```bash
docker compose logs backend
```

3. **Verify CORS settings** in `backend/main.py`

### Slow Build Times

**Problem:** `docker compose build` takes forever

**Solutions:**

1. **Check .dockerignore files exist** (see implementation guide)

2. **Use BuildKit:**
```bash
DOCKER_BUILDKIT=1 docker compose build
```

3. **Clear cache:**
```bash
docker builder prune
```

### Containers Won't Start

**Problem:** Services immediately exit

**Solutions:**

1. **Check logs:**
```bash
docker compose logs
```

2. **Try building without cache:**
```bash
docker compose build --no-cache
docker compose up
```

3. **Check Docker is running:**
```bash
docker info
```

## Getting Help

If none of these solutions work:

1. **Check container status:**
```bash
docker compose ps
```

2. **Get detailed logs:**
```bash
docker compose logs --tail=100
```

3. **Inspect configuration:**
```bash
docker compose config
```

4. **Try clean slate:**
```bash
docker compose down -v
docker system prune -f
docker compose up --build
```
```

### Step 4.4: Update .gitignore

Ensure `.gitignore` includes Docker artifacts:

```bash
# Add to .gitignore if not present
echo "" >> .gitignore
echo "# Docker" >> .gitignore
echo ".dockerignore" >> .gitignore
```

Actually, keep `.dockerignore` in git:
```bash
# Just ensure these are in .gitignore:
# (They should already be there)
.env
data/
node_modules/
__pycache__/
```

---

## Testing & Validation

### Pre-Flight Checklist

Before marking implementation complete, verify all items:

#### Build & Startup
- [ ] `docker compose build` succeeds for both services
- [ ] `docker compose up` starts both services without errors
- [ ] Backend becomes healthy within 40 seconds
- [ ] Frontend starts after backend health check passes
- [ ] Both services accessible from browser

#### Functionality
- [ ] Frontend loads at http://localhost:5173
- [ ] Backend API responds at http://localhost:8001
- [ ] Can create a new conversation
- [ ] Can submit query to council
- [ ] Stage 1: Individual LLM responses appear
- [ ] Stage 2: Reviews appear
- [ ] Stage 3: Final response appears
- [ ] Sidebar shows all conversations

#### Hot Reload
- [ ] Edit Python file in `backend/` → backend reloads
- [ ] Edit React file in `frontend/src/` → browser updates
- [ ] Changes visible within 2 seconds
- [ ] No manual container restart needed

#### Data Persistence
- [ ] Create a test conversation
- [ ] Stop containers (`docker compose down`)
- [ ] Restart containers (`docker compose up`)
- [ ] Test conversation still exists
- [ ] Can create new conversations
- [ ] Data files visible in `data/conversations/`

#### Environment & Configuration
- [ ] `.env` file loaded correctly
- [ ] API key visible in backend logs (first 20 chars)
- [ ] OpenRouter API calls succeed
- [ ] No placeholder API key errors

#### Developer Experience
- [ ] `./docker-start.sh` script works
- [ ] `docker compose logs -f` shows both services
- [ ] `docker compose down` cleanly shuts down
- [ ] `docker compose up -d` (background mode) works
- [ ] README instructions are clear

#### Error Handling
- [ ] Graceful shutdown with Ctrl+C
- [ ] Helpful error messages for missing .env
- [ ] Helpful error messages for port conflicts
- [ ] Health checks work correctly

### Validation Script

Create `project management/validate-docker.sh`:

```bash
#!/bin/bash

echo "🧪 LLM Council Docker Validation"
echo "================================"
echo ""

# Test 1: Docker is running
echo "Test 1: Checking Docker..."
if docker info > /dev/null 2>&1; then
    echo "  ✅ Docker is running"
else
    echo "  ❌ Docker is not running"
    exit 1
fi

# Test 2: .env file exists
echo "Test 2: Checking .env file..."
if [ -f .env ]; then
    echo "  ✅ .env file exists"
else
    echo "  ❌ .env file missing"
    exit 1
fi

# Test 3: Build containers
echo "Test 3: Building containers..."
if docker compose build > /dev/null 2>&1; then
    echo "  ✅ Containers build successfully"
else
    echo "  ❌ Build failed"
    exit 1
fi

# Test 4: Start containers
echo "Test 4: Starting containers..."
docker compose up -d
sleep 10

# Test 5: Backend health
echo "Test 5: Checking backend health..."
if curl -s http://localhost:8001/health > /dev/null; then
    echo "  ✅ Backend is healthy"
else
    echo "  ❌ Backend not responding"
    docker compose down
    exit 1
fi

# Test 6: Frontend responding
echo "Test 6: Checking frontend..."
if curl -s http://localhost:5173 > /dev/null; then
    echo "  ✅ Frontend is responding"
else
    echo "  ❌ Frontend not responding"
    docker compose down
    exit 1
fi

# Test 7: Cleanup
echo "Test 7: Stopping containers..."
docker compose down
echo "  ✅ Cleanup successful"

echo ""
echo "🎉 All validation tests passed!"
```

Make it executable:
```bash
chmod +x project management/validate-docker.sh
```

Run validation:
```bash
./project management/validate-docker.sh
```

---

## Rollback Strategy

If containerization causes issues, you can easily revert:

### Immediate Rollback

```bash
# Stop Docker containers
docker compose down

# Use original startup method
./start.sh

# Or manually:
# Terminal 1:
uv run python -m backend.main

# Terminal 2:
cd frontend && npm run dev
```

### Files to Keep

The following files are **additive only** and don't modify existing functionality:
- `backend.Dockerfile`
- `frontend/frontend.Dockerfile`
- `docker-compose.yml`
- `.dockerignore`
- `frontend/.dockerignore`
- `docker-start.sh`

**Modified files** (can revert from git):
- `frontend/vite.config.js` (added Docker-friendly settings)
- `README.md` (added Docker instructions)

### Full Rollback

```bash
# If on containerization branch
git checkout main

# If committed to main
git revert <commit-hash>

# Or manually remove files
rm backend.Dockerfile
rm frontend/frontend.Dockerfile
rm docker-compose.yml
rm docker-start.sh
rm .dockerignore
rm frontend/.dockerignore
git restore frontend/vite.config.js
git restore README.md
```

---

## Post-Implementation

### Documentation Tasks

- [ ] Update `README.md` with Docker instructions (Step 4.2)
- [ ] Add troubleshooting guide (Step 4.3)
- [ ] Update `CLAUDE.md` if present
- [ ] Create GitHub issue templates for Docker-related bugs

### Knowledge Sharing

- [ ] Document lessons learned
- [ ] Note any OrbStack-specific optimizations discovered
- [ ] Share performance benchmarks (native vs Docker)

### Optional Enhancements

#### Production Dockerfiles

Create production-optimized variants:
- `backend.prod.Dockerfile` with multi-stage build
- `frontend.prod.Dockerfile` with static build
- Separate `docker-compose.prod.yml`

#### CI/CD Integration

- GitHub Actions to build Docker images
- Automated testing in containers
- Push images to Docker Hub or GitHub Container Registry

#### Monitoring

- Add logging configuration
- Set up health check dashboards
- Monitor container resource usage

---

## Timeline

### Week 1

**Day 1-2: Backend (Phase 1)**
- Create Dockerfile
- Test build and run
- Verify hot reload

**Day 3-4: Frontend (Phase 2)**
- Create Dockerfile
- Update Vite config
- Test build and run

**Day 5: Integration (Phase 3)**
- Create docker-compose.yml
- Test orchestration
- Validate all functionality

### Week 2

**Day 1-2: Polish (Phase 4)**
- Create helper scripts
- Update documentation
- Troubleshooting guide

**Day 3-4: Testing**
- Complete validation checklist
- Test on clean machine
- Fix any issues

**Day 5: Release**
- Final testing
- Update main README
- Communicate to team

---

## Success Metrics

After implementation, measure:

1. **Setup Time**
   - Target: < 10 minutes for new developer
   - Measure: Time from clone to running app

2. **Development Speed**
   - Target: < 2 seconds for hot reload
   - Measure: Time from save to browser update

3. **Stability**
   - Target: Zero container crashes in normal operation
   - Measure: Uptime during development sessions

4. **Documentation Quality**
   - Target: New developer can follow README without help
   - Measure: Feedback from testing with fresh user

---

## Appendix

### File Checklist

By the end of implementation, these files should exist:

```
llm-council/
├── backend.Dockerfile               ✅ Phase 1
├── frontend/
│   └── frontend.Dockerfile          ✅ Phase 2
├── docker-compose.yml               ✅ Phase 3
├── .dockerignore                    ✅ Phase 1
├── frontend/.dockerignore           ✅ Phase 2
├── docker-start.sh                  ✅ Phase 4
├── README.md (updated)              ✅ Phase 4
└── project management/
    ├── PRD.md                       ✅ Pre-existing
    ├── TechnicalSpec.md             ✅ Pre-existing
    ├── ImplementationPlan.md        ✅ This document
    ├── Docker-Troubleshooting.md    ✅ Phase 4
    └── validate-docker.sh           ✅ Phase 4 (validation)
```

### Quick Reference Commands

```bash
# Build
docker compose build
docker compose build --no-cache backend

# Run
docker compose up
docker compose up -d
docker compose up --build

# Monitor
docker compose ps
docker compose logs
docker compose logs -f backend
docker compose top

# Manage
docker compose restart
docker compose stop
docker compose down
docker compose down -v  # Also remove volumes

# Debug
docker compose exec backend /bin/bash
docker compose exec frontend /bin/sh
docker compose config

# Cleanup
docker system prune
docker builder prune
```

### Related Documents

- [v1.1 PRD](./PRD-v1.1.md) - Product requirements
- [v1.1 Technical Specification](./TechnicalSpec-v1.1.md) - Architecture details
- [Product Overview](../../ProductOverview.md) - System-wide documentation
- [Docker Troubleshooting](./Docker-Troubleshooting.md) - Created in Phase 4
- [Project Conventions](../../ProjectConventions.md) - Development standards
- [Main README](../../../README.md) - User documentation

---

**Implementation Status:** Not Started  
**Last Updated:** December 24, 2025  
**Ready to Begin:** Yes ✅

