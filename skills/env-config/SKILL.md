---
name: "env-config"
description: "Defines environment variable conventions for backend and frontend. Invoke when adding config, secrets, startup validation, or `.env.example` updates."
---

# Environment Configuration

Use this skill when a feature introduces new environment variables or depends on runtime configuration.

## Core Rules
- Keep a committed `.env.example` with every required variable.
- Never commit `.env` or production secrets.
- Validate configuration on startup, not lazily during request handling.
- Expose only true client-safe values through `NEXT_PUBLIC_*`.

## Backend Pattern
Use `pydantic-settings` with one centralized settings object.

```python
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str
    jwt_secret_key: str
    google_client_id: str
```

Rules:
- Instantiate settings once and inject or import from a single module.
- Keep defaults only for non-sensitive local-development values.
- Fail fast when required values are missing.

## Frontend Pattern
Use a typed env parser for browser-exposed config, for example `zod`.

```ts
import { z } from "zod";

const envSchema = z.object({
  NEXT_PUBLIC_BACKEND_URL: z.string().url(),
  NEXT_PUBLIC_GTM_ID: z.string().min(1).optional(),
});

export const env = envSchema.parse({
  NEXT_PUBLIC_BACKEND_URL: process.env.NEXT_PUBLIC_BACKEND_URL,
  NEXT_PUBLIC_GTM_ID: process.env.NEXT_PUBLIC_GTM_ID,
});
```

Rules:
- Read `process.env` in one place only.
- Re-export typed values from a shared env module.
- Do not access non-`NEXT_PUBLIC_*` vars in client code.

## Naming Conventions
- Use uppercase snake case.
- Group related vars by domain: auth, db, payments, analytics, storage.
- Keep names explicit: `LEMONSQUEEZY_WEBHOOK_SECRET` is better than `WEBHOOK_SECRET`.

## Documentation
Every feature doc should include:
- Variable name
- Whether it is required
- Example value format
- Whether it is server-only or browser-exposed

## Checklist
- [ ] Add new keys to `.env.example`
- [ ] Validate backend env on startup
- [ ] Validate frontend env in one shared module
- [ ] Restrict browser vars to `NEXT_PUBLIC_*`
- [ ] Avoid scattered `os.getenv()` and raw `process.env` usage
