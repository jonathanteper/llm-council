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

