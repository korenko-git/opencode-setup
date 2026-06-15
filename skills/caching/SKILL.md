---
name: caching
version: 1.0
tags: [backend, redis, performance]
description: "Redis patterns, TTL policies, cache invalidation. Use when adding caching to a service."
---

# Caching with Redis

Redis caching standards.

---

## 1. Dependencies

```bash
uv add redis[hiredis]
```

---

## 2. Connection (app/core/redis.py)

```python
from __future__ import annotations

import redis.asyncio as redis
from app.core.config import settings

_redis: redis.Redis | None = None


async def get_redis() -> redis.Redis:
    global _redis
    if _redis is None:
        _redis = redis.from_url(
            settings.redis_url,
            encoding="utf-8",
            decode_responses=True,
        )
    return _redis


async def close_redis() -> None:
    global _redis
    if _redis:
        await _redis.aclose()
        _redis = None
```

```python
# app/main.py
@app.on_event("startup")
async def startup():
    await get_redis()  # warmup connection

@app.on_event("shutdown")
async def shutdown():
    await close_redis()
```

---

## 3. Patterns

### Cache-Aside (Read-Through)

Primary pattern: check the cache; on a miss, read from the DB and populate the cache:

```python
import json
from app.core.redis import get_redis

async def get_user(user_id: int) -> dict:
    r = await get_redis()
    key = f"user:{user_id}"
    
    cached = await r.get(key)
    if cached:
        return json.loads(cached)
    
    user = await db.fetch_user(user_id)  # DB
    await r.setex(key, 300, json.dumps(user))  # TTL 5 minutes
    return user
```

### Write-Through

Update the cache together with the DB:

```python
async def update_user(user_id: int, data: dict) -> dict:
    user = await db.update_user(user_id, data)
    r = await get_redis()
    await r.setex(f"user:{user_id}", 300, json.dumps(user))
    return user
```

### Cache Invalidation

Invalidate when data changes:

```python
async def delete_user(user_id: int) -> None:
    await db.delete_user(user_id)
    r = await get_redis()
    await r.delete(f"user:{user_id}")
    # Invalidate related keys
    await r.delete(f"user:{user_id}:orders")
```

### Pattern invalidation (be careful in prod)

```python
# ONLY for dev / small key sets
async def invalidate_user_cache(user_id: int) -> None:
    r = await get_redis()
    keys = await r.keys(f"user:{user_id}:*")
    if keys:
        await r.delete(*keys)
```

> ⚠️ `KEYS` blocks Redis. In production, use `SCAN` to search by pattern.

---

## 4. TTL Policies

| Data type | TTL | Notes |
|---|---|---|
| User profile | 5 min | Changes infrequently |
| Session | 60 min | Resets on activity |
| List (paginated) | 1 min | Stales quickly |
| Config / feature flags | 10 min | Changes infrequently |
| Rate limit counter | 60 sec | Sliding window |
| OTP / temporary token | 10 min | Explicit invalidation after use |

---

## 5. Rate Limiting

```python
async def check_rate_limit(user_id: int, action: str, limit: int = 10, window: int = 60) -> bool:
    r = await get_redis()
    key = f"rate:{action}:{user_id}"
    count = await r.incr(key)
    if count == 1:
        await r.expire(key, window)
    return count <= limit

# Usage
if not await check_rate_limit(user.id, "send_email", limit=5, window=3600):
    raise HTTPException(429, "Too many requests")
```

---

## 6. Key Naming

Format: `{entity}:{id}:{subtype}` — always predictable and hierarchical:

```
user:42                    # profile
user:42:orders             # user orders
rate:send_email:42         # rate limit
session:abc123             # session
config:feature_flags       # config
```

- No spaces in keys.
- Use underscores inside segments, colons between segments.
- Put `entity` first — simplifies searching and debugging.

---

## 7. Environment Variables

```env
REDIS_URL=redis://localhost:6379/0
```

```python
class Settings(BaseSettings):
    redis_url: str = "redis://localhost:6379/0"
```
