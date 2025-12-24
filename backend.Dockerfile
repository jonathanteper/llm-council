# Backend Dockerfile for LLM Council
# Implements: FR-1.1 (Backend Dockerfile)
# 
# This Dockerfile creates a containerized environment for the FastAPI backend
# using Python 3.11-slim and the uv package manager.

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install uv package manager
# Using the official installation script from astral.sh
RUN pip install --no-cache-dir uv

# Copy dependency files first (for Docker layer caching)
COPY pyproject.toml uv.lock* ./

# Install Python dependencies using uv
# This creates a virtual environment and installs all packages
RUN uv sync --frozen

# Copy backend source code
# Note: In development, this will be overridden by volume mount
COPY backend/ ./backend/

# Expose port 8001 for FastAPI application
EXPOSE 8001

# Health check for container orchestration (FR-1.3)
# Docker will use this to determine if the container is healthy
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8001/health')"

# Run the FastAPI application using uv
# Bind to 0.0.0.0 to accept connections from outside the container
CMD ["uv", "run", "python", "-m", "backend.main"]

