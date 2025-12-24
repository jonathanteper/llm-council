# LLM Council

Multi-LLM query processing system with council-based deliberation.

## 🚀 Quick Start

### Docker (Recommended)

```bash
docker compose up
```

Access the application at `http://localhost:5173`

### Native Development

```bash
# Start both backend and frontend
bash scripts/start.sh
```

## 📚 Documentation

- **[Full Documentation](docs/README.md)** - Complete project documentation
- **[API Reference](docs/API.md)** - REST API documentation
- **[Skills Setup](docs/skills/SETUP.md)** - Development workflow automation
- **[Project Management](project%20management/)** - PRDs, specs, and plans

## 🏗️ Project Structure

```
llm-council/
├── backend/              # FastAPI backend
├── frontend/             # React frontend
├── tests/                # Test suite
├── docs/                 # Documentation
├── scripts/              # Utility scripts
├── project management/   # Product documentation
└── utilities/            # Development utilities
```

## ⚙️ Configuration

Create a `.env` file:

```bash
OPENROUTER_API_KEY=sk-or-v1-...
```

## 🧪 Testing

```bash
# Backend tests
pytest tests/backend/

# Frontend tests
cd frontend && npm test

# With coverage
pytest --cov=backend --cov-report=term-missing
```

## 🛠️ Development

See [full documentation](docs/README.md) for:
- Architecture overview
- Development workflow
- Code standards
- Contribution guidelines

## 📋 Features

- **Multi-LLM Processing**: Query multiple AI models simultaneously
- **Three-Stage Deliberation**: Initial responses → Cross-examination → Synthesis
- **Conversation History**: Persistent conversation storage
- **Docker Support**: Containerized development and deployment
- **Hot Reload**: Fast development iteration
- **Comprehensive Testing**: 90%+ test coverage

## 🔗 Quick Links

- [Backend API](http://localhost:8001) - FastAPI backend
- [Frontend](http://localhost:5173) - React frontend
- [API Docs](http://localhost:8001/docs) - Interactive API documentation

---

**Version**: 1.2 | **License**: MIT | **Status**: Active Development
