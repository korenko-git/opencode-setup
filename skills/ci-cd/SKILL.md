---
name: ci-cd
version: 1.0
tags: [devops, github-actions, automation]
description: "GitHub Actions pipelines: linting, tests, Docker build, deployment. Use when setting up CI/CD for a new project."
---

# CI/CD with GitHub Actions

Standard pipelines for lint → test → build → deploy.

---

## 1. Workflow Structure

```
.github/
  workflows/
    ci.yml          # lint + test on every PR
    deploy.yml      # build image and deploy on main
    release.yml     # tag → GitHub Release (optional)
```

---

## 2. ci.yml — Lint + Test

```yaml
name: CI

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  lint-backend:
    name: Lint Backend
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: backend
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v4
        with:
          version: "latest"
      - run: uv sync --frozen
      - run: uv run ruff check .
      - run: uv run ruff format --check .
      - run: uv run mypy .

  lint-frontend:
    name: Lint Frontend
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: frontend
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v3
        with:
          version: 9
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: pnpm
          cache-dependency-path: frontend/pnpm-lock.yaml
      - run: pnpm install --frozen-lockfile
      - run: pnpm lint
      - run: pnpm tsc --noEmit

  test-backend:
    name: Test Backend
    runs-on: ubuntu-latest
    needs: lint-backend
    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    defaults:
      run:
        working-directory: backend
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v4
      - run: uv sync --frozen
      - run: uv run pytest --tb=short
        env:
          DATABASE_URL: postgresql://test:test@localhost:5432/test
```

---

## 3. deploy.yml — Docker Build + Deploy

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  build-and-push:
    name: Build & Push Docker
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@v4

      - name: Log in to GHCR
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and push backend
        uses: docker/build-push-action@v5
        with:
          context: ./backend
          push: true
          tags: ghcr.io/${{ github.repository }}/backend:latest
          cache-from: type=registry,ref=ghcr.io/${{ github.repository }}/backend:cache
          cache-to: type=registry,ref=ghcr.io/${{ github.repository }}/backend:cache,mode=max

  deploy:
    name: Deploy to Server
    runs-on: ubuntu-latest
    needs: build-and-push
    steps:
      - name: SSH deploy
        uses: appleboy/ssh-action@v1
        with:
          host: ${{ secrets.DEPLOY_HOST }}
          username: ${{ secrets.DEPLOY_USER }}
          key: ${{ secrets.DEPLOY_SSH_KEY }}
          script: |
            cd /opt/app
            docker compose pull
            docker compose up -d --remove-orphans
            docker system prune -f
```

---

## 4. Secrets (Settings → Secrets)

| Secret | Purpose |
|---|---|
| `DEPLOY_HOST` | Server IP / hostname |
| `DEPLOY_USER` | SSH user |
| `DEPLOY_SSH_KEY` | Private SSH key |
| `GITHUB_TOKEN` | Automatically available for GHCR |

---

## 5. Rules

- CI runs on every PR; deploy only from `main`.
- Lint always runs before tests (`needs: lint-backend`).
- Cache Docker layers via `cache-from`/`cache-to` in GHCR.
- Use `actions/checkout@v4`, `setup-node@v4` — pinned major versions.
- `pnpm tsc --noEmit` is required in CI for TypeScript projects.
- Never store secrets in code — only via `${{ secrets.* }}`.
