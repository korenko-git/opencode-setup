---
name: logging
version: 1.0
tags: [backend, observability, python]
description: "Structured logs, levels, correlation IDs. Use when setting up logging in backend services."
---

# Logging

Structured logging standards.

---

## 1. Library: structlog

```bash
uv add structlog
```

---

## 2. Configuration (app/core/logging.py)

```python
from __future__ import annotations

import logging
import sys

import structlog


def setup_logging(*, json_logs: bool = False, log_level: str = "INFO") -> None:
    shared_processors: list[structlog.types.Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
    ]

    if json_logs:
        renderer = structlog.processors.JSONRenderer()
    else:
        renderer = structlog.dev.ConsoleRenderer(colors=True)

    structlog.configure(
        processors=shared_processors + [structlog.stdlib.ProcessorFormatter.wrap_for_formatter],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        structlog.stdlib.ProcessorFormatter(
            processors=[structlog.stdlib.ProcessorFormatter.remove_processors_meta, renderer],
        )
    )

    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(log_level)
```

Call on application startup:

```python
# app/main.py
from app.core.logging import setup_logging
from app.core.config import settings

setup_logging(json_logs=settings.log_json, log_level=settings.log_level)
```

---

## 3. Correlation ID (Request ID)

Every HTTP request gets a unique `request_id`, which is propagated through all logs:

```python
# app/middleware/logging.py
import uuid
import structlog
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

logger = structlog.get_logger()

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(
            request_id=request_id,
            method=request.method,
            path=request.url.path,
        )
        
        logger.info("request_started")
        response = await call_next(request)
        logger.info("request_finished", status_code=response.status_code)
        
        response.headers["X-Request-ID"] = request_id
        return response
```

Enable in `app/main.py`:
```python
app.add_middleware(RequestLoggingMiddleware)
```

---

## 4. Usage in Code

```python
import structlog

logger = structlog.get_logger(__name__)

# Correct — structured fields
logger.info("user_created", user_id=user.id, email=user.email)
logger.warning("payment_retry", attempt=3, order_id=order.id)
logger.error("stripe_error", error_code=err.code, order_id=order.id)

# Incorrect — string interpolation
logger.info(f"Created user {user.id} with email {user.email}")  # ❌
```

---

## 5. Log Levels

| Level | When to use |
|---|---|
| `DEBUG` | Development details; disabled in prod |
| `INFO` | Key events: created, started, finished |
| `WARNING` | Unexpected situation, but the app continues |
| `ERROR` | Error in a specific operation; the whole service does not crash |
| `CRITICAL` | Catastrophe — the service cannot continue |

---

## 6. What NOT to Log

- Passwords, tokens, API keys
- Full payment data (card numbers, CVV)
- Personal data beyond what is necessary (passport, phone)
- Raw SQL queries containing user data

---

## 7. Environment Variables

```env
LOG_LEVEL=INFO          # DEBUG / INFO / WARNING / ERROR
LOG_JSON=true           # true in prod, false in dev
```

```python
class Settings(BaseSettings):
    log_level: str = "INFO"
    log_json: bool = False
```

---

## 8. Production Log Format (JSON)

```json
{
  "event": "user_created",
  "user_id": 42,
  "email": "user@example.com",
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "level": "info",
  "timestamp": "2024-01-15T10:30:00.123456Z",
  "logger": "app.services.users"
}
```
