---
name: api-design
version: 1.0
tags: [backend, api, openapi]
description: "REST/OpenAPI conventions, versioning, response structure. Use when designing new API endpoints."
---

# API Design

REST API design standards.

---

## 1. URL Conventions

- Resources are plural nouns: `/users`, `/orders`, `/products`.
- Nested hierarchy: `/users/{id}/orders/{order_id}`.
- No verbs in URLs — actions are expressed via HTTP methods.
- Lowercase + hyphen only: `/payment-methods`, not `paymentMethods`.

```
GET    /users              # list
POST   /users              # create
GET    /users/{id}         # get one
PATCH  /users/{id}         # partial update
DELETE /users/{id}         # delete
```

---

## 2. Versioning

Put the version in the URL prefix:

```
/api/v1/users
/api/v2/users
```

- The current version is always `v1` (or higher).
- Do not break existing contracts — adding fields is allowed; removals only in a new version.
- Deprecated endpoints: respond with headers `Deprecation: true` and `Sunset: <date>`.

---

## 3. Response Shape

### Success response

```json
{
  "data": { ... },
  "meta": {
    "request_id": "550e8400-e29b-41d4-a716-446655440000"
  }
}
```

### List with pagination

```json
{
  "data": [ ... ],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 143,
    "total_pages": 8
  },
  "meta": {
    "request_id": "..."
  }
}
```

### Error

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed",
    "details": [
      { "field": "email", "message": "Invalid email format" }
    ]
  },
  "meta": {
    "request_id": "..."
  }
}
```

---

## 4. HTTP Status Codes

| Scenario | Code |
|---|---|
| Successful creation | 201 |
| Successful read/update | 200 |
| Delete (no body) | 204 |
| Invalid data | 422 |
| Unauthorized | 401 |
| Forbidden | 403 |
| Not found | 404 |
| Conflict (duplicate) | 409 |
| Server error | 500 |

---

## 5. OpenAPI / FastAPI

Document every endpoint via `summary`, `description`, `response_model`:

```python
@router.post(
    "/users",
    response_model=UserResponse,
    status_code=201,
    summary="Create user",
    description="Creates a new user. Email must be unique.",
    responses={
        409: {"description": "User with this email already exists"},
    },
)
async def create_user(body: CreateUserRequest) -> UserResponse:
    ...
```

- All Pydantic schemas include `description` on every field.
- Use `tags` for grouping in Swagger UI.
- The OpenAPI schema is available at `/api/openapi.json`.

---

## 6. Field Naming

- JSON fields use `snake_case`.
- Dates use ISO 8601: `"created_at": "2024-01-15T10:30:00Z"`.
- Money uses integers in the smallest currency unit (cents/kopecks): `"amount": 1500`.
- Boolean fields: `is_active`, `has_access`, `can_edit`.

---

## 7. Filtering and Sorting

```
GET /users?is_active=true&role=admin
GET /orders?sort=created_at&order=desc
GET /products?page=2&per_page=20
GET /events?from=2024-01-01&to=2024-12-31
```

---

## 8. New Endpoint Checklist

- [ ] URL uses a plural noun
- [ ] Correct HTTP method
- [ ] `response_model` is set
- [ ] `summary` / `description` documentation
- [ ] Errors use correct status codes
- [ ] `request_id` exists in `meta` for every response
- [ ] Fields are in `snake_case`
- [ ] Added to the correct `tags` group
