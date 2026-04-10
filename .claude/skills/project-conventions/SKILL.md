---
name: project-conventions
description: Enforces Temis-RiskControl project conventions for backend architecture, file placement, naming, and stack usage. Invoke before adding features, new files, or modifying existing layers.
---

# Temis-RiskControl — Project Conventions

When working in this project, always follow the rules below. Do not deviate unless the user explicitly asks.

---

## Stack

- **Backend**: Python 3.12 + FastAPI + Uvicorn
- **Config**: Pydantic `BaseSettings` — never hardcode values, always read from environment
- **Frontend**: Not yet implemented — do not scaffold it unless asked
- **Agent**: Not yet implemented — do not scaffold it unless asked

---

## Backend Folder Structure

All backend code lives inside `backend/app/`. Respect the layered architecture:

| Folder | What belongs here |
|---|---|
| `api/` | FastAPI route handlers and the router aggregator (`router.py`) |
| `core/` | App-wide config, settings, startup logic |
| `database/` | DB connection setup, session factories |
| `entities/` | Domain/business entities (pure Python classes, no DB coupling) |
| `models/` | Pydantic request/response schemas |
| `repositories/` | Data access — all queries go here, never in routes |
| `infra/` | External service clients (email, storage, third-party APIs) |

### Rules

- Never put business logic directly in `api/` route handlers — delegate to a service or repository
- Never import from `api/` inside `repositories/`, `entities/`, or `models/` — dependencies flow downward only
- New endpoints must be registered in `backend/app/api/router.py`, not mounted directly in `main.py`
- All API routes must be prefixed with `/api/`

---

## Naming Conventions

- **Files**: `snake_case.py`
- **Classes**: `PascalCase`
- **Functions and variables**: `snake_case`
- **Pydantic models**: suffix with `Request`, `Response`, or `Schema` (e.g., `CreateUserRequest`, `UserResponse`)
- **Repository classes**: suffix with `Repository` (e.g., `UserRepository`)
- **Entity classes**: no suffix, plain domain name (e.g., `User`, `RiskEvent`)

---

## Environment Variables

- Never hardcode secrets or config values
- All variables must have a corresponding entry in `backend/.env.example`
- Read them through the Pydantic `Settings` class in `backend/app/core/config.py`


## What NOT to do

- Do not create files outside their designated layer folder
- Do not add dependencies to `requirements.txt` without a clear reason — ask the user first
- Do not implement frontend or agent features unless explicitly asked
- Do not skip `.env.example` updates when adding new environment variables
- Do not add endpoints directly in `main.py` — always go through `router.py`
