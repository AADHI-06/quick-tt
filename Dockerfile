# Stage 1: Build Frontend
FROM node:18-alpine as frontend-build
WORKDIR /app
COPY web/package.json web/package-lock.json ./
RUN npm ci
COPY web/ ./
RUN npm run build

# Stage 2: Setup Backend
FROM python:3.11-slim
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY timetable_system/ ./timetable_system/
COPY api/ ./api/

# Copy frontend build artifacts
COPY --from=frontend-build /app/dist ./web/dist

# Environment variables
ENV TT_DB_PASSWORD=placeholder

# Run the application
CMD ["sh", "-c", "uvicorn api.main:app --host 0.0.0.0 --port ${PORT:-8080}"]
