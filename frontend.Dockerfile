# Frontend Dockerfile for LLM Council
# Implements: FR-2.1 (Frontend Dockerfile)
# 
# This Dockerfile creates a containerized environment for the React/Vite frontend
# using Node 20-alpine for a minimal image size.

FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy package files first (for Docker layer caching)
COPY frontend/package*.json ./

# Install npm dependencies
# --no-optional skips optional dependencies
# --legacy-peer-deps resolves any peer dependency conflicts
RUN npm install --legacy-peer-deps

# Copy frontend source code
# Note: In development, this will be overridden by volume mount
COPY frontend/ ./

# Expose port 5173 for Vite dev server
EXPOSE 5173

# Start Vite dev server
# --host 0.0.0.0 binds to all interfaces (required for container access)
# This is configured in vite.config.js (FR-2.3)
CMD ["npm", "run", "dev"]

