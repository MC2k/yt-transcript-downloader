# Stage 1: Build frontend
FROM node:20-alpine AS frontend-builder
WORKDIR /frontend

# Accept build argument
ARG NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
ENV NEXT_PUBLIC_BACKEND_URL=$NEXT_PUBLIC_BACKEND_URL

# Copy package files
COPY frontend/package.json frontend/package-lock.json ./

# Install dependencies (dev included for build)
RUN npm ci

# Copy all frontend files at once
COPY frontend/ ./

# Build Next.js
RUN npm run build

# Prune to production only
RUN npm prune --production

# Stage 2: Python runtime
FROM python:3.11-slim

WORKDIR /app

# Install Node.js runtime and npm
RUN apt-get update && apt-get install -y --no-install-recommends nodejs npm && rm -rf /var/lib/apt/lists/*

# Copy backend
COPY backend/ ./backend/
COPY transcript_extractor.py .
COPY requirements.txt .

# Install Python deps
RUN pip install --no-cache-dir -r requirements.txt

# Copy built frontend from builder
COPY --from=frontend-builder /frontend/.next ./frontend/.next
COPY --from=frontend-builder /frontend/public ./frontend/public
COPY --from=frontend-builder /frontend/package.json ./frontend/
COPY --from=frontend-builder /frontend/node_modules ./frontend/node_modules

# Startup script
RUN printf '#!/bin/sh\ncd /app && python -m flask --app backend.app run --host 0.0.0.0 --port 8000 &\ncd /app/frontend && npm start &\nwait\n' > /app/start.sh && chmod +x /app/start.sh

EXPOSE 3001 8000

CMD ["/app/start.sh"]