# Build stage for frontend
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Final stage
FROM python:3.11-slim
WORKDIR /app

# Install Node.js runtime for frontend serving
RUN apt-get update && apt-get install -y nodejs npm && rm -rf /var/lib/apt/lists/*

# Copy backend
COPY backend/ ./backend/
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy frontend build from builder stage
COPY --from=frontend-builder /app/frontend/.next ./frontend/.next
COPY --from=frontend-builder /app/frontend/public ./frontend/public
COPY --from=frontend-builder /app/frontend/package.json ./frontend/

# Install frontend dependencies for production
WORKDIR /app/frontend
RUN npm install --production

# Create startup script
WORKDIR /app
RUN echo '#!/bin/sh\n\
    cd /app/backend && python -m flask --app app run --host 0.0.0.0 --port 5000 &\n\
    cd /app/frontend && npm start\n\
    wait' > /app/start.sh && chmod +x /app/start.sh

EXPOSE 3000 8000

CMD ["/app/start.sh"]