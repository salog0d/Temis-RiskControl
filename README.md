# Temis RiskControl

> Real-time risk assessment and fraud prevention platform powered by a multi-stage AI decision pipeline.

Temis RiskControl combines a **FastAPI async backend** for entity management with an **ADK agent pipeline** that evaluates transactions through sequential risk assessment, decision-making, and automated action stages.

---

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Repository Layout](#repository-layout)
- [Backend API](#backend-api)
- [Agent Pipeline](#agent-pipeline)
- [Getting Started](#getting-started)
- [Running Tests](#running-tests)
- [CI/CD](#cicd)
- [Documentation](#documentation)
- [Contributing](#contributing)

---

## Architecture Overview

The platform is organized into two primary code tracks that operate together:

| Component | Stack | Responsibility |
|-----------|-------|----------------|
| **Backend** | FastAPI · SQLAlchemy (async) · PostgreSQL | CRUD API for users, accounts, and devices |
| **Agent** | ADK Pipeline | Multi-stage risk evaluation: `risk_engine → decision_engine → action_engine` |

### Data Model

The relational model is built around three core entities with cascading relationships:

- **Usuario** — End users subject to risk evaluation.
- **Cuenta** — Financial accounts linked to a user (`ForeignKey` with `CASCADE` delete).
- **Dispositivo** — Registered devices linked to a user, tracked for fingerprinting and anomaly detection.

> For the full schema rationale, constraints, and migration history, see [`docs/database-design.pdf`](docs/database-design.pdf).

---

## Repository Layout

```
.
├── agent/                          # AI-powered risk pipeline
│   └── risk_control_pipeline/
│       └── agent.py                # Stage sequencing: risk → decision → action
├── backend/
│   ├── app/
│   │   ├── api/                    # Route definitions
│   │   ├── core/                   # Settings, configuration, security
│   │   ├── database/               # Session management, engine setup
│   │   ├── entities/               # Pydantic schemas (request/response)
│   │   ├── infra/                  # Infrastructure adapters
│   │   ├── models/                 # SQLAlchemy ORM models
│   │   └── repositories/          # Data access layer
│   └── tests/                      # Unit and integration tests
├── docs/                           # Design documents and diagrams
├── frontend/                       # Client application (planned)
├── scripts/                        # Utility and automation scripts
└── .github/workflows/
    └── ci.yml                      # Continuous integration pipeline
```

---

## Backend API

**Base URL:** `/api`

### Health

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/health` | Service health check |

### Usuarios

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/usuarios` | Create a new user |
| `GET` | `/api/usuarios` | List all users |
| `GET` | `/api/usuarios/{id}` | Retrieve user by ID |
| `PATCH` | `/api/usuarios/{id}` | Update user fields |
| `DELETE` | `/api/usuarios/{id}` | Remove user |

### Cuentas

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/cuentas` | Create a new account |
| `GET` | `/api/cuentas` | List all accounts |
| `GET` | `/api/cuentas/{id}` | Retrieve account by ID |
| `PATCH` | `/api/cuentas/{id}` | Update account fields |
| `DELETE` | `/api/cuentas/{id}` | Remove account |

### Dispositivos

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/dispositivos` | Register a new device |
| `GET` | `/api/dispositivos` | List all devices |
| `GET` | `/api/dispositivos/{id}` | Retrieve device by ID |
| `PATCH` | `/api/dispositivos/{id}` | Update device fields |
| `POST` | `/api/dispositivos/{id}/touch` | Record device activity timestamp |
| `DELETE` | `/api/dispositivos/{id}` | Remove device |

---

## Agent Pipeline

The risk control agent follows a sequential three-stage architecture where each stage has a well-defined input/output contract. The pipeline is implemented in `agent/risk_control_pipeline/agent.py`.

### Agent State Machine

<img width="3585" height="629" alt="Agent state machine diagram showing the risk_engine → decision_engine → action_engine pipeline" src="https://github.com/user-attachments/assets/f4af7d5e-4639-46e7-8a2c-b6cbad6a521c" />

The stage sequencing provides clear separation of concerns between risk assessment, policy evaluation, and action execution.

---

## Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL (or a compatible async-supported database)
- A `.env` file containing only fields declared in the `Settings` class

### Installation

```bash
# Clone the repository
git clone https://github.com/<org>/temis-riskcontrol.git
cd temis-riskcontrol

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # macOS/Linux
# .venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt
```

### Running the Server

```bash
export PYTHONPATH=backend
uvicorn app.main:app --reload --app-dir backend
```

The API will be available at `http://localhost:8000`. Interactive documentation is served at `/docs` (Swagger UI) and `/redoc`.

---

## Running Tests

```bash
PYTHONPATH=backend pytest backend/tests -v
```

---

## CI/CD

The GitHub Actions workflow (`.github/workflows/ci.yml`) runs the following jobs on every push and pull request:

1. **Backend checks** — Dependency installation, compilation verification, and smoke tests.
2. **Test suite** — Full `pytest` run against the backend.
3. **Docker build** — Validates that the container image builds successfully.

---

## Diagrams

### Stack Diagram

<img width="2751" height="2017" alt="Stack diagram showing components and integration boundaries" src="https://github.com/user-attachments/assets/c7dee67a-3626-4b46-847c-ca3024b06e33" />

High-level representation of components and integration boundaries. Matches the current split between backend and agent pipeline.

### Relational Model

<img width="2023" height="1776" alt="Relational model diagram showing usuario, cuenta, and dispositivo entities" src="https://github.com/user-attachments/assets/3cc397a9-a04a-4778-b6c6-49ab19f1c932" />

The model reflects the implemented entities (`usuario`, `cuenta`, `dispositivo`) with relationships consistent with `ForeignKey(... ondelete="CASCADE")` usage.

### Database Design Document

For the complete schema rationale, constraint definitions, and migration history, see [`docs/database-design.pdf`](docs/database-design.pdf).

---

## Contributing

### Branch and PR Naming

Follow the sprint-based naming convention:

```
Sprint#-ShortDescription
```

Examples: `Sprint2-ImplementLogin`, `Sprint3-AddFraudDetectionRules`

Each pull request should represent **one feature or fix**, be small enough for a meaningful review, and include a description with context and evidence where relevant.

### Commit Messages

This project uses [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(scope): short description
```

| Type | Purpose |
|------|---------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation changes |
| `chore` | Maintenance and dependency updates |
| `refactor` | Internal improvements (no behavior change) |
| `test` | Test additions or modifications |

Examples:

```
feat(auth): add login endpoint
fix(api): handle null response in transaction service
docs(readme): update setup instructions
```

---