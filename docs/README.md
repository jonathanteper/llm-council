# LLM Council - Full Documentation

Multi-LLM query processing system with council-based deliberation.

## Documentation Index

- **[API Reference](./API.md)** - Complete API documentation
- **[Claude Integration](./CLAUDE.md)** - Using Claude with this project
- **[Skills Setup](./skills/SETUP.md)** - Setting up vibe-coding skill
- **[Skills Migration Guide](./skills/MIGRATION.md)** - Migration reference

## Project Overview

LLM Council is a sophisticated system that processes queries through multiple Large Language Models (LLMs) in three deliberation stages:

1. **Stage 1: Initial Responses** - Multiple LLMs provide independent answers
2. **Stage 2: Cross-Examination** - Models critique each other's responses
3. **Stage 3: Synthesis** - Final consolidated answer with citations

## Architecture

- **Backend**: FastAPI-based REST API (`backend/`)
- **Frontend**: React/Vite SPA (`frontend/`)
- **Storage**: JSON-based conversation persistence (`data/`)
- **Testing**: Comprehensive test suite (`tests/`)
- **Deployment**: Docker containerization

## Quick Start

See main [README.md](../README.md) in project root for quick start instructions.

## Development

### Running Tests

```bash
# Backend tests
pytest tests/backend/

# Frontend tests
cd frontend && npm test

# All tests with coverage
pytest --cov=backend --cov-report=term-missing
```

### Docker Development

```bash
# Start all services
docker compose up

# Rebuild after changes
docker compose up --build

# View logs
docker compose logs -f backend
docker compose logs -f frontend
```

### Native Development

```bash
# Start both services
bash scripts/start.sh

# Or manually:
# Terminal 1: Backend
uv run python -m backend.main

# Terminal 2: Frontend
cd frontend && npm run dev
```

## Project Structure

```
llm-council/
├── backend/              # FastAPI backend
│   ├── main.py          # Application entry point
│   ├── council.py       # Council orchestration logic
│   ├── openrouter.py    # LLM integration
│   ├── storage.py       # Data persistence
│   └── config.py        # Configuration
├── frontend/            # React frontend
│   └── src/
│       ├── components/  # React components
│       └── api.js       # Backend API client
├── tests/               # Test suite
│   ├── backend/         # Backend tests
│   └── frontend/        # Frontend tests
├── docs/                # Documentation (you are here)
├── scripts/             # Utility scripts
├── project management/  # Product docs (PRDs, specs)
└── utilities/           # Development utilities
```

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
OPENROUTER_API_KEY=sk-or-v1-...
```

### Supported LLMs

The system supports any model available through OpenRouter. Common choices:

- GPT-4 (OpenAI)
- Claude 3.5 Sonnet (Anthropic)
- Gemini Pro (Google)
- Llama models (Meta)

## Contributing

### Development Workflow

1. Create feature branch
2. Write tests first (TDD)
3. Implement feature
4. Ensure 90%+ test coverage
5. Update documentation
6. Submit PR

See [Project Conventions](../project%20management/ProjectConventions.md) for detailed standards.

### Code Standards

- **Python**: PEP 8, type hints, docstrings
- **JavaScript**: ESLint, functional components, hooks
- **Git**: Conventional commits with requirement references
- **Testing**: 90%+ coverage target

## Resources

- **Project Management**: See `project management/` folder
  - PRDs for each version
  - Technical specifications
  - Implementation plans
  - Test plans

- **Skills**: See `docs/skills/`
  - Development process automation
  - Team workflow standards

## Support

For issues or questions:
1. Check documentation in this folder
2. Review project management documents
3. Check test files for usage examples
4. Open an issue on the repository

---

**Last Updated**: December 24, 2025  
**Version**: 1.2  
**Status**: Active Development

