# Product Requirements Document: LLM Council v1.1 - Containerization

**Version:** 1.1  
**Date:** December 24, 2025  
**Status:** In Progress  
**Owner:** Development Team

---

## Executive Summary

This document outlines the product requirements for containerizing the LLM Council application using Docker and OrbStack. The goal is to improve developer experience, eliminate dependency conflicts, and prepare the application for potential cloud deployment while maintaining all existing functionality.

---

## Goals & Motivation

### Primary Goals

1. **Eliminate Dependency Conflicts**
   - Remove the need for developers to manage multiple Python versions
   - Eliminate Node.js version conflicts between projects
   - Isolate uv package manager dependencies from host system

2. **Simplify Developer Experience**
   - Enable one-command startup for the entire application stack
   - Reduce onboarding time for new developers
   - Minimize "works on my machine" issues

3. **Cloud Deployment Readiness**
   - Create a foundation for easy deployment to cloud platforms
   - Establish containerization patterns that scale to production
   - Make the application portable across different environments

4. **Learning & Best Practices**
   - Understand containerization workflows in a real-world project
   - Learn Docker Compose orchestration patterns
   - Establish knowledge base for future projects

### Why Now?

- The application stack (Python/FastAPI + Node.js/React) is stable and working
- Multiple Cursor-built projects would benefit from consistent containerization
- OrbStack provides excellent macOS performance for container development
- Current setup requires coordinating two separate development servers manually

---

## User Stories

### Developer Stories

**Story 1: Simple Setup**
> As a **new developer** joining the project,  
> I want to **start the entire application with a single command**,  
> So that I can **begin contributing without spending hours on environment setup**.

**Acceptance Criteria:**
- Running `docker compose up` (or equivalent) starts both backend and frontend
- No Python or Node.js installation required on host machine
- Setup instructions are clear and take less than 10 minutes

**Story 2: Development Hot Reload**
> As a **developer** actively coding,  
> I want my **code changes to immediately reflect in the running application**,  
> So that I can **maintain my development flow without manual restarts**.

**Acceptance Criteria:**
- Python file changes in `backend/` trigger automatic reload
- React component changes in `frontend/` trigger hot module replacement
- No noticeable performance degradation compared to native execution

**Story 3: Data Persistence**
> As a **developer** testing the application,  
> I want my **conversation data and API configuration to persist across container restarts**,  
> So that I don't **lose my work or have to reconfigure every time**.

**Acceptance Criteria:**
- Conversations stored in `data/conversations/` persist after container stop/start
- `.env` file with API key works without modification
- No data is lost when containers are rebuilt

### Future Deployment Stories

**Story 4: Cloud Deployment**
> As a **user** wanting to deploy to the cloud,  
> I want the **application pre-configured for containerized deployment**,  
> So that I can **easily deploy to platforms like Fly.io, Railway, or AWS**.

**Acceptance Criteria:**
- Container images can be built for production use
- Environment variables can be externalized for cloud platforms
- Application runs consistently in development and production modes

---

## Requirements

### Functional Requirements

#### FR-1: Backend Containerization

The system shall containerize the FastAPI backend application.

**Priority:** P0 (Must Have)  
**Status:** In Progress

##### FR-1.1: Backend Dockerfile

The system shall provide a Dockerfile that:
- Uses Python 3.11-slim as base image
- Installs uv package manager
- Installs Python dependencies from pyproject.toml
- Exposes port 8001
- Runs backend with `uv run python -m backend.main`

**Priority:** P0 (Must Have)  
**Status:** In Progress

##### FR-1.2: Backend Volume Mounts

The system shall mount host directories into backend container:
- `./backend` → `/app/backend` (source code, read-write)
- `./data` → `/app/data` (conversation storage, read-write)
- `./.env` → `/app/.env` (environment config, read-only)

**Priority:** P0 (Must Have)  
**Status:** In Progress

##### FR-1.3: Backend Health Check

The system shall provide health check endpoint:
- Endpoint: `GET /health`
- Returns service status
- Used by Docker for container orchestration

**Priority:** P0 (Must Have)  
**Status:** In Progress

#### FR-2: Frontend Containerization

The system shall containerize the React/Vite frontend application.

**Priority:** P0 (Must Have)  
**Status:** In Progress

##### FR-2.1: Frontend Dockerfile

The system shall provide a Dockerfile that:
- Uses Node 20-alpine as base image
- Installs npm dependencies
- Exposes port 5173
- Runs Vite dev server with `--host 0.0.0.0`

**Priority:** P0 (Must Have)  
**Status:** In Progress

##### FR-2.2: Frontend Volume Mounts

The system shall mount host directories into frontend container:
- `./frontend` → `/app` (source code, read-write)
- Anonymous volume for `/app/node_modules` (preserve container deps)

**Priority:** P0 (Must Have)  
**Status:** In Progress

##### FR-2.3: Frontend HMR Configuration

The system shall configure Vite for Hot Module Replacement in containers:
- Server binds to `0.0.0.0` (not localhost)
- HMR WebSocket configured for container networking
- File watching works with volume mounts

**Priority:** P0 (Must Have)  
**Status:** In Progress

#### FR-3: Docker Compose Orchestration

The system shall provide Docker Compose configuration for multi-container management.

**Priority:** P0 (Must Have)  
**Status:** In Progress

##### FR-3.1: Service Definitions

The system shall define services in docker-compose.yml:
- Backend service with build context and configuration
- Frontend service with build context and configuration
- Shared bridge network for inter-container communication

**Priority:** P0 (Must Have)  
**Status:** In Progress

##### FR-3.2: Service Dependencies

The system shall configure service startup order:
- Frontend depends on backend health check
- Backend starts first and becomes healthy
- Frontend starts only after backend is ready

**Priority:** P0 (Must Have)  
**Status:** In Progress

##### FR-3.3: Port Mapping

The system shall map container ports to host:
- Backend: Container 8001 → Host 8001
- Frontend: Container 5173 → Host 5173

**Priority:** P0 (Must Have)  
**Status:** In Progress

#### FR-4: Development Workflow

The system shall maintain developer-friendly workflow.

**Priority:** P0 (Must Have)  
**Status:** In Progress

##### FR-4.1: Hot Reload Support

The system shall support hot reload for both services:
- Python code changes trigger backend reload via Uvicorn
- React code changes trigger frontend HMR via Vite
- Changes reflect within 2 seconds

**Priority:** P0 (Must Have)  
**Status:** In Progress

##### FR-4.2: Data Persistence

The system shall persist data across container lifecycle:
- Conversations in `data/conversations/` survive restarts
- Environment variables from `.env` remain accessible
- No data loss on container stop/start/rebuild

**Priority:** P0 (Must Have)  
**Status:** In Progress

##### FR-4.3: Single Command Startup

The system shall enable single-command startup:
- `docker compose up` starts both services
- Logs from both services visible in terminal
- Ctrl+C gracefully shuts down both services

**Priority:** P0 (Must Have)  
**Status:** In Progress

#### FR-5: Documentation & Developer Experience

The system shall provide comprehensive documentation.

**Priority:** P1 (Should Have)  
**Status:** In Progress

##### FR-5.1: Docker Instructions

The system shall provide README documentation for:
- Docker setup steps
- Comparison with native workflow
- Troubleshooting common issues

**Priority:** P1 (Should Have)  
**Status:** In Progress

##### FR-5.2: Build Optimization

The system shall provide `.dockerignore` files:
- Exclude unnecessary files from build context
- Reduce image size and build time
- Separate ignore files for backend and frontend

**Priority:** P1 (Should Have)  
**Status:** In Progress

##### FR-5.3: Helper Scripts

The system may provide optional helper scripts:
- `docker-start.sh` wrapper for convenience
- Validation script to test setup
- Pre-flight checks for common issues

**Priority:** P2 (Nice to Have)  
**Status:** Planned

---

### Non-Functional Requirements

#### NFR-1: Performance

The containerized application shall maintain acceptable performance.

**Priority:** P0 (Must Have)  
**Status:** In Progress

##### NFR-1.1: Startup Time

The system shall start containers within acceptable time:
- Both services running within 30 seconds
- Backend healthy within 40 seconds
- Frontend accessible within 60 seconds

**Priority:** P0 (Must Have)  
**Status:** In Progress

##### NFR-1.2: Hot Reload Speed

The system shall provide fast hot reload:
- Code changes detected within 1 second
- Application reloaded within 2 seconds total
- No significant delay vs native workflow

**Priority:** P0 (Must Have)  
**Status:** In Progress

##### NFR-1.3: Runtime Performance

The system shall have minimal performance overhead:
- API response times match native (< 5ms overhead)
- No noticeable CPU/memory increase
- File I/O performance acceptable for development

**Priority:** P1 (Should Have)  
**Status:** In Progress

#### NFR-2: Compatibility

The system shall maintain backward compatibility and platform support.

**Priority:** P0 (Must Have)  
**Status:** In Progress

##### NFR-2.1: Native Workflow Compatibility

The system shall preserve native development workflow:
- Original `start.sh` continues to work
- No changes to backend/frontend source code
- Users can choose Docker or native at will

**Priority:** P0 (Must Have)  
**Status:** In Progress

##### NFR-2.2: OrbStack Optimization

The system shall be optimized for OrbStack on macOS:
- File watching works without polling
- Volume mounts perform well
- Resource usage is efficient

**Priority:** P1 (Should Have)  
**Status:** In Progress

##### NFR-2.3: Docker Desktop Support

The system should work with Docker Desktop:
- All functionality available
- May require polling for file watching
- Performance may be slower but acceptable

**Priority:** P1 (Should Have)  
**Status:** In Progress

#### NFR-3: Reliability

The system shall be stable and reliable for development use.

**Priority:** P0 (Must Have)  
**Status:** In Progress

##### NFR-3.1: Container Stability

The system shall run without crashes:
- No random container exits during normal operation
- Graceful error handling for common issues
- Clear error messages for debugging

**Priority:** P0 (Must Have)  
**Status:** In Progress

##### NFR-3.2: Data Integrity

The system shall protect user data:
- No data loss on container restart
- Atomic writes to conversation files
- .env file mounted read-only for safety

**Priority:** P0 (Must Have)  
**Status:** In Progress

#### NFR-4: Usability

The system shall be easy to use for developers.

**Priority:** P1 (Should Have)  
**Status:** In Progress

##### NFR-4.1: Setup Simplicity

The system shall have simple setup:
- New developer running in < 10 minutes
- Clear error messages if setup fails
- Minimal prerequisites (just OrbStack + .env)

**Priority:** P1 (Should Have)  
**Status:** In Progress

##### NFR-4.2: Documentation Quality

The system shall have clear documentation:
- README instructions work without help
- Troubleshooting guide addresses common issues
- Examples show actual commands

**Priority:** P1 (Should Have)  
**Status:** In Progress

---

## Success Criteria

### Must Have (P0)

- ✅ Single command (`docker compose up`) starts both frontend and backend
- ✅ Backend accessible at `http://localhost:8001`
- ✅ Frontend accessible at `http://localhost:5173`
- ✅ Hot reload functional for both Python and React code
- ✅ Existing `.env` file works without changes
- ✅ Conversation data persists in `data/conversations/`
- ✅ API calls to OpenRouter work correctly from containerized backend

### Should Have (P1)

- ✅ Clear documentation in README on both native and Docker startup
- ✅ `.dockerignore` files to optimize build times
- ✅ Health checks for service orchestration
- ✅ Graceful shutdown of both services with Ctrl+C
- ✅ Error messages that help debug common issues

### Nice to Have (P2)

- 🔄 Startup script wrapper (`docker-start.sh`) for convenience
- 🔄 Troubleshooting guide for common Docker/OrbStack issues
- 🔄 Performance comparison documentation (native vs containerized)
- 🔄 Optional production-ready Dockerfile variants

### Metrics for Success

1. **Setup Time**: New developer can run app in < 10 minutes
2. **Development Speed**: Hot reload takes < 2 seconds
3. **Reliability**: No random failures requiring container rebuild
4. **Documentation**: README instructions work for non-Docker experts

---

## Non-Goals & Out of Scope

### Version 1.0 Out of Scope

❌ **Production Deployment Configuration**
- Not including production-optimized Dockerfiles
- Not setting up CI/CD pipelines
- Not configuring container orchestration (Kubernetes, ECS)

❌ **Database Containerization**
- Application uses JSON file storage, no database needed
- No Redis, PostgreSQL, or other data services

❌ **Advanced Networking**
- No SSL/TLS configuration
- No reverse proxy setup (nginx, tracelane)
- No multi-container networking beyond basic compose

❌ **Monitoring & Observability**
- No logging aggregation
- No metrics collection (Prometheus, Grafana)
- No distributed tracing

❌ **Security Hardening**
- Using development containers, not production-hardened
- API key still in `.env` file (acceptable for local dev)
- No secrets management system

### Future Considerations

These may be addressed in later versions:
- Production deployment recipes for common platforms
- Automated testing in containers
- Multi-stage builds for optimized images
- Container registry publishing

---

## Technical Constraints

### Platform Requirements

- **Primary Platform**: macOS with OrbStack
- **Alternative**: Docker Desktop (should work but not optimized for)
- **Not Supporting**: Windows WSL2 (may work, but untested)

### Compatibility Requirements

- Must maintain compatibility with existing native development workflow
- Original `start.sh` script must continue to work
- No breaking changes to existing codebase
- Same port numbers (8001, 5173) to avoid frontend config changes

### Performance Requirements

- Container startup time: < 30 seconds for both services
- Hot reload response: < 2 seconds
- No significant CPU/memory overhead vs native
- File watching must work reliably on macOS

---

## Dependencies & Assumptions

### External Dependencies

1. **OrbStack** - Primary container runtime (Docker-compatible)
2. **Docker Compose** - Multi-container orchestration
3. **OpenRouter API** - External LLM service (unchanged)

### Assumptions

1. Users have basic terminal/command-line familiarity
2. `.env` file with valid API key already exists
3. Internet connection available for pulling base images
4. macOS file system performance sufficient for volume mounts
5. Port 8001 and 5173 are available on host

---

## User Experience Flow

### Current Experience (Native)

```
1. Install Python 3.10+
2. Install uv package manager
3. Run: uv sync
4. Install Node.js
5. Run: cd frontend && npm install
6. Create .env file with API key
7. Run: ./start.sh (or manually start two terminals)
8. Access http://localhost:5173
```

**Pain Points:**
- Multiple manual steps
- Dependency version conflicts
- Two terminal windows to manage
- Platform-specific issues

### Target Experience (Containerized)

```
1. Install OrbStack
2. Clone repository
3. Create .env file with API key
4. Run: docker compose up
5. Access http://localhost:5173
```

**Improvements:**
- Fewer steps (5 vs 8)
- No language runtime installation
- Single command for entire stack
- Consistent experience across machines

---

## Risk Assessment

### Technical Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| File watching doesn't work on macOS | Low | High | OrbStack handles this well; test thoroughly |
| Slow performance vs native | Medium | Medium | Use volume mounts, not COPY; benchmark early |
| Port conflicts with existing services | Low | Low | Document port requirements; provide override options |
| .env file not loading in container | Low | High | Test multiple mount strategies; clear documentation |

### Adoption Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Developers prefer native workflow | Medium | Medium | Keep both options; show clear benefits |
| OrbStack not available/installed | Medium | Low | Provide Docker Desktop fallback instructions |
| Confusion about when to use each method | Medium | Low | Clear documentation on use cases |

---

## Timeline & Milestones

### Phase 1: Core Implementation (Week 1)
- Create Dockerfiles for backend and frontend
- Create docker-compose.yml
- Verify hot reload functionality

### Phase 2: Documentation & Polish (Week 1-2)
- Update README with Docker instructions
- Create troubleshooting guide
- Add .dockerignore files

### Phase 3: Validation (Week 2)
- Test on fresh machine
- Gather feedback from developers
- Address any issues

---

## Open Questions

1. Should we provide both development and production Dockerfiles initially, or just development?
   - **Decision**: Development only for v1.0

2. What's the preferred command: `docker compose up` or a wrapper script like `./docker-start.sh`?
   - **Decision**: Both - direct command in docs, optional wrapper for convenience

3. Should we commit docker-compose.yml or provide it as a template?
   - **Decision**: Commit it - it's part of the standard development workflow

---

## Appendix

### Related Documents

### Version Documentation
- [Product Overview](../../ProductOverview.md) - System-wide documentation
- [v1.0 PRD](../v1.0/PRD-v1.0.md) - Core functionality (prerequisite)
- [Technical Specification](./TechnicalSpec-v1.1.md) - v1.1 architecture details
- [Implementation Plan](./ImplementationPlan-v1.1.md) - v1.1 step-by-step guide

### Project Documentation
- [Project Conventions](../../ProjectConventions.md) - Development standards
- [Main README](../../../README.md) - User-facing documentation

### Glossary
- **OrbStack**: Fast, lightweight container runtime for macOS
- **Hot Reload**: Automatic application update when code changes
- **Volume Mount**: Mapping host filesystem directory into container
- **Docker Compose**: Tool for defining multi-container applications

