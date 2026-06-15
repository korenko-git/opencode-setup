---
name: docker
version: 1.0
tags: [devops, infrastructure]
description: "Dockerfile, docker-compose, healthcheck standards. Use when containerizing services or setting up environments."
---

# Docker

Project containerization standards.

---

## 1. Dockerfile — Backend (Python/FastAPI)

```dockerfile
# ---- build stage ----
FROM python:3.12-slim AS builder
WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN pip install uv && uv sync --frozen --no-dev

# ---- runtime stage ----
FROM python:3.12-slim
WORKDIR /app

# Non-root user
RUN addgroup --system app && adduser --system --ingroup app app

COPY --from=builder /app/.venv .venv
COPY app/ ./app/

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

USER app

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import httpx; httpx.get('http://localhost:8000/health').raise_for_status()"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 2. Dockerfile — Frontend (Next.js)

```dockerfile
FROM node:20-alpine AS deps
WORKDIR /app
COPY package.json pnpm-lock.yaml ./
RUN corepack enable && pnpm install --frozen-lockfile

FROM node:20-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN pnpm build

FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
RUN addgroup --system app && adduser --system --ingroup app app
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public
USER app

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
  CMD wget -qO- http://localhost:3000/api/health || exit 1

CMD ["node", "server.js"]
```

## 3. docker-compose.yml

```yaml
services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    env_file: .env
    ports:
      - "8000:8000"
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "python", "-c", "import httpx; httpx.get('http://localhost:8000/health').raise_for_status()"]
      interval: 30s
      timeout: 5s
      start_period: 10s
      retries: 3
    restart: unless-stopped

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    env_file: .env
    ports:
      - "3000:3000"
    depends_on:
      backend:
        condition: service_healthy
    restart: unless-stopped

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    command: redis-server --save 60 1 --loglevel warning
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
```

## 4. Правила

## 4. Rules
- Non-root пользователь в production образах.
- Always use multi-stage builds — separate `builder` and minimal `runner`.
- Use a non-root user in production images.
- Every service has a `healthcheck`; dependent services use `condition: service_healthy`.
- `.dockerignore` is required: exclude `.git`, `.venv`, `node_modules`, `__pycache__`, `*.pyc`.
- Use `env_file: .env` for secrets, not inline `environment:` values.
- Use `restart: unless-stopped` for all production services.
- Use named volumes for persistent data.

## 5. .dockerignore (template)

```
.git
.gitignore
.env*
!.env.example
__pycache__
*.pyc
.venv
node_modules
.next
*.log
dist
build
DOCKERFILE.md
```

## 6. Useful Commands

```bash
# Bring everything up (with rebuild)
docker compose up --build -d

# View healthcheck statuses
docker compose ps

# Logs for a specific service
docker compose logs -f backend

# Exec into a container
docker compose exec backend bash

# Stop and remove volumes (careful!)
docker compose down -v
```
