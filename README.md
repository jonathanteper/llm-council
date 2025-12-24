# LLM Council

![llmcouncil](header.jpg)

The idea of this repo is that instead of asking a question to your favorite LLM provider (e.g. OpenAI GPT 5.1, Google Gemini 3.0 Pro, Anthropic Claude Sonnet 4.5, xAI Grok 4, eg.c), you can group them into your "LLM Council". This repo is a simple, local web app that essentially looks like ChatGPT except it uses OpenRouter to send your query to multiple LLMs, it then asks them to review and rank each other's work, and finally a Chairman LLM produces the final response.

In a bit more detail, here is what happens when you submit a query:

1. **Stage 1: First opinions**. The user query is given to all LLMs individually, and the responses are collected. The individual responses are shown in a "tab view", so that the user can inspect them all one by one.
2. **Stage 2: Review**. Each individual LLM is given the responses of the other LLMs. Under the hood, the LLM identities are anonymized so that the LLM can't play favorites when judging their outputs. The LLM is asked to rank them in accuracy and insight.
3. **Stage 3: Final response**. The designated Chairman of the LLM Council takes all of the model's responses and compiles them into a single final answer that is presented to the user.

## Vibe Code Alert

This project was 99% vibe coded as a fun Saturday hack because I wanted to explore and evaluate a number of LLMs side by side in the process of [reading books together with LLMs](https://x.com/karpathy/status/1990577951671509438). It's nice and useful to see multiple responses side by side, and also the cross-opinions of all LLMs on each other's outputs. I'm not going to support it in any way, it's provided here as is for other people's inspiration and I don't intend to improve it. Code is ephemeral now and libraries are over, ask your LLM to change it in whatever way you like.

## Setup

### 1. Install Dependencies

The project uses [uv](https://docs.astral.sh/uv/) for project management.

**Backend:**
```bash
uv sync
```

**Frontend:**
```bash
cd frontend
npm install
cd ..
```

### 2. Configure API Key

Create a `.env` file in the project root:

```bash
OPENROUTER_API_KEY=sk-or-v1-...
```

Get your API key at [openrouter.ai](https://openrouter.ai/). Make sure to purchase the credits you need, or sign up for automatic top up.

### 3. Configure Models (Optional)

Edit `backend/config.py` to customize the council:

```python
COUNCIL_MODELS = [
    "openai/gpt-5.1",
    "google/gemini-3-pro-preview",
    "anthropic/claude-sonnet-4.5",
    "x-ai/grok-4",
]

CHAIRMAN_MODEL = "google/gemini-3-pro-preview"
```

## Running the Application

### Option 1: Docker (Recommended) 🐳

The easiest way to run the application is with Docker Compose. This method requires minimal setup and works consistently across different machines.

**Prerequisites:**
- [Docker](https://www.docker.com/) or [OrbStack](https://orbstack.dev/) (recommended for macOS)
- A `.env` file with your OpenRouter API key (see setup above)

**Start the application:**
```bash
docker compose up
```

That's it! The command will:
- Build both backend and frontend containers
- Start both services with hot reload enabled
- Make the app available at http://localhost:5173
- Keep your data persistent in the `data/` directory

**Stop the application:**
```bash
# Press Ctrl+C in the terminal where docker compose is running
# Or in a different terminal:
docker compose down
```

**Benefits of Docker:**
- ✅ No need to install Python, Node.js, or uv
- ✅ Consistent environment across all machines
- ✅ Hot reload works for both backend and frontend
- ✅ Data persists across container restarts
- ✅ One command to start everything

### Option 2: Native Development

If you prefer to run the application natively without Docker:

**Use the start script:**
```bash
./start.sh
```

**Or run manually:**

Terminal 1 (Backend):
```bash
uv run python -m backend.main
```

Terminal 2 (Frontend):
```bash
cd frontend
npm run dev
```

Then open http://localhost:5173 in your browser.

**Native Prerequisites:**
- Python 3.10+ with [uv](https://docs.astral.sh/uv/) installed
- Node.js 20+ with npm
- Dependencies installed (see Setup section above)

## Tech Stack

- **Backend:** FastAPI (Python 3.10+), async httpx, OpenRouter API
- **Frontend:** React + Vite, react-markdown for rendering
- **Storage:** JSON files in `data/conversations/`
- **Package Management:** uv for Python, npm for JavaScript
- **Containerization:** Docker + Docker Compose (optional)

## Development

### Hot Reload

Both Docker and native development support hot reload:
- **Backend**: Python file changes trigger automatic uvicorn reload
- **Frontend**: React component changes trigger Vite HMR (Hot Module Replacement)

Changes should be reflected in your browser within 1-2 seconds.

### Project Structure

```
llm-council/
├── backend/              # FastAPI backend
│   ├── main.py          # API server
│   ├── council.py       # Council orchestration logic
│   ├── config.py        # Model configuration
│   └── storage.py       # JSON file storage
├── frontend/            # React frontend
│   ├── src/
│   │   ├── components/  # React components
│   │   └── api.js       # Backend API client
│   └── vite.config.js   # Vite configuration
├── data/                # Persistent conversation data
│   └── conversations/
├── docker-compose.yml   # Docker orchestration
├── backend.Dockerfile   # Backend container
└── frontend.Dockerfile  # Frontend container
```

### Troubleshooting

**Docker Issues:**

- **Port already in use**: Stop any services using ports 8001 or 5173
  ```bash
  docker compose down
  # Or check what's using the port:
  lsof -i :8001
  lsof -i :5173
  ```

- **Changes not reflecting**: Ensure volume mounts are working
  ```bash
  docker compose down
  docker compose up --build
  ```

- **See logs**:
  ```bash
  docker compose logs backend
  docker compose logs frontend
  ```

**Native Issues:**

- **Backend won't start**: Check your `.env` file exists and has valid API key
- **Frontend build errors**: Delete `node_modules` and run `npm install` again
- **Port conflicts**: Make sure nothing else is using ports 8001 or 5173
