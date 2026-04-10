# Temis RiskControl

> Real-time fraud detection and risk prevention platform powered by a multi-stage AI decision pipeline.

Temis RiskControl combines a **FastAPI async backend** for entity management with a **Google ADK agent pipeline** that evaluates transactions through sequential risk scoring, policy decision, and automated enforcement stages.

---

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Tech Stack](#tech-stack)
- [Repository Layout](#repository-layout)
- [Data Model](#data-model)
- [Backend API](#backend-api)
- [Agent Pipeline](#agent-pipeline)
  - [Stage 1 — Risk Engine](#stage-1--risk-engine)
  - [Stage 2 — Decision Engine](#stage-2--decision-engine)
  - [Stage 3 — Action Engine](#stage-3--action-engine)
- [Frontend](#frontend)
- [Observability](#observability)
  - [Metrics](#metrics)
  - [Alerting](#alerting)
  - [Dashboards](#dashboards)
- [Environment Variables](#environment-variables)
- [Getting Started](#getting-started)
- [Running Tests](#running-tests)
- [CI/CD](#cicd)
- [Diagrams](#diagrams)
- [Contributing](#contributing)

---

## Architecture Overview

The platform is organized into three primary tracks that operate together:

| Component | Stack | Responsibility |
|-----------|-------|----------------|
| **Backend** | FastAPI · SQLAlchemy (async) · PostgreSQL | CRUD API, webhook ingestion, enforcement endpoints |
| **Agent** | Google ADK · Gemini 2.5 Flash | Multi-stage risk pipeline: `risk_engine → decision_engine → action_engine` |
| **Frontend** | React 19 · TypeScript · Vite | Dashboard and transaction monitoring UI |
| **Observability** | Prometheus · Grafana · AlertManager | Metrics collection, dashboards, and alert routing |

### Request Flow

```
Client / Transaction Stream
        │
        ▼
POST /api/webhook/transaction
        │
        ▼
  Backend API (FastAPI)
        │  forwards via httpx
        ▼
  Agent Service (port 9000)
        │
        ├─► Stage 1: Risk Engine Agent   → risk_assessment (score + signals)
        ├─► Stage 2: Decision Engine     → decision (verdict + rule)
        └─► Stage 3: Action Engine       → action_result (enforcement log)
                          │
                          ▼
              POST /api/enforcement/*  (block, rate-limit, notify)
```

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| **Backend** | Python 3.12 · FastAPI · SQLAlchemy (async) · Pydantic Settings |
| **Database** | PostgreSQL (asyncpg) · SQLite (aiosqlite, dev) |
| **Agent Pipeline** | Google ADK · Gemini 2.5 Flash LLM |
| **Frontend** | React 19 · TypeScript · Vite · React Router 7 · Framer Motion |
| **Infrastructure** | Docker · Docker Compose · uvicorn |
| **Observability** | Prometheus v2.51 · Grafana v10.4 · AlertManager v0.27 |
| **Testing** | pytest · pytest-asyncio |
| **CI/CD** | GitHub Actions |

---

## Repository Layout

```
.
├── agent/
│   └── risk_control_pipeline/
│       ├── agent.py                      # Root SequentialAgent (3-stage orchestrator)
│       ├── agents/
│       │   ├── risk_engine_agent.py      # Stage 1: fraud scoring (10 signals)
│       │   ├── decision_engine_agent.py  # Stage 2: policy rules → verdict
│       │   └── action_engine_agent.py    # Stage 3: enforcement actions
│       └── tools/
│           ├── risk_scoring_tools.py     # 10 fraud scoring functions
│           └── action_tools.py           # block, rate-limit, invalidate, notify
├── backend/
│   ├── app/
│   │   ├── api/                          # Route modules (15+)
│   │   ├── core/
│   │   │   └── config.py                 # Pydantic Settings (reads .env)
│   │   ├── database/                     # Async engine, session factory
│   │   ├── models/                       # Pydantic request/response schemas
│   │   ├── infra/                        # Adapters: agent_client, email_client
│   │   └── repositories/                 # Data access layer (per-entity CRUD)
│   ├── tests/
│   └── pytest.ini
├── frontend/
│   ├── src/
│   │   ├── types/                        # TypeScript interfaces
│   │   ├── hooks/                        # useRiskAction, useAuth, useMutation, …
│   │   ├── mocks/                        # Dev mock data
│   │   └── components/
│   ├── package.json
│   └── vite.config.ts
├── infra/
│   ├── prometheus/
│   │   ├── prometheus.yml                # Scrape config + 15-day retention
│   │   └── alert_rules.yml               # 4 alert rules (ServiceDown, ErrorRate, Latency, RequestRate)
│   ├── alertmanager/
│   │   └── alertmanager.yml              # SMTP routing by severity (critical/warning)
│   └── grafana/
│       ├── provisioning/
│       │   ├── datasources/              # Auto-provisions Prometheus datasource
│       │   └── dashboards/               # Auto-loads dashboard provider
│       └── dashboards/
│           └── temis_overview.json       # Request rate, latency percentiles, handler throughput
├── docs/
│   └── database-design.pdf
├── .env.example
├── docker-compose.yml
└── .github/workflows/ci.yml
```

---

## Data Model

The relational model centers on three core entities with cascading relationships, extended by supporting tables for the full fraud lifecycle.

### Core Entities

| Entity | Description | Key Fields |
|--------|-------------|------------|
| **Usuario** | End users subject to risk evaluation | id, email, telefono, status, last_login, rate_limit fields, session_invalidated_at |
| **Cuenta** | Financial accounts linked to a user | id, user_id (FK CASCADE), balance, currency, status |
| **Dispositivo** | Registered devices for fingerprinting | id, user_id (FK CASCADE), fingerprint, trusted, first_seen, last_seen |
| **Transaccion** | Transaction records | id, user_id (FK), from_account_id, to_account, amount, currency, status, ip, device_id |
| **Beneficiario** | Destination accounts for transfers | id, user_id (FK), account_number, account_holder, status |

### Risk & Fraud Tables

| Entity | Description |
|--------|-------------|
| **RiskAssessment** | Pipeline output per transaction (risk_score, risk_level, signal breakdown) |
| **RiskFeature** | Individual signal values stored for auditability |
| **FraudAction** | Enforcement outcomes (action_type, status, linked to RiskAssessment) |

### Auth & Security Tables

| Entity | Description |
|--------|-------------|
| **OtpChallenge** | MFA challenges (code, method sms/email, status, expires_at) |
| **Session** | Active user sessions |
| **TokenBlacklist** | Revoked JWT tokens |
| **SecurityEvent** | Audit trail of auth events (password change, OTP failure, etc.) |
| **AuditLog** | Full event trail of API-level decisions and mutations |
| **IpReputation** | IP risk scores, VPN/TOR flags, provider metadata |

> For full schema rationale, constraints, and migration history see [`docs/database-design.pdf`](docs/database-design.pdf).

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
| `POST` | `/api/usuarios` | Create user |
| `GET` | `/api/usuarios` | List users |
| `GET` | `/api/usuarios/{id}` | Get user by ID |
| `PATCH` | `/api/usuarios/{id}` | Update user fields |
| `DELETE` | `/api/usuarios/{id}` | Delete user |

### Cuentas

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/cuentas` | Create account |
| `GET` | `/api/cuentas` | List accounts |
| `GET` | `/api/cuentas/{id}` | Get account by ID |
| `PATCH` | `/api/cuentas/{id}` | Update account fields |
| `DELETE` | `/api/cuentas/{id}` | Delete account |

### Dispositivos

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/dispositivos` | Register device |
| `GET` | `/api/dispositivos` | List devices |
| `GET` | `/api/dispositivos/{id}` | Get device by ID |
| `PATCH` | `/api/dispositivos/{id}` | Update device fields |
| `POST` | `/api/dispositivos/{id}/touch` | Record device activity timestamp |
| `DELETE` | `/api/dispositivos/{id}` | Delete device |

### Transacciones

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/transacciones` | Create transaction record |
| `GET` | `/api/transacciones` | List transactions (filterable by `user_id`) |
| `GET` | `/api/transacciones/{id}` | Get transaction by ID |
| `PATCH` | `/api/transacciones/{id}` | Update transaction |
| `DELETE` | `/api/transacciones/{id}` | Delete transaction |

### Webhook (Pipeline Entry Point)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/webhook/transaction` | Submit transaction event to the risk pipeline |

The webhook accepts a `TransactionEventRequest` payload carrying the nine risk signal inputs. It returns `202 Accepted` immediately and forwards the event to the Agent service via async HTTP.

### Enforcement

Called internally by the Action Engine agent after a verdict is reached. Also exposed for direct integration.

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/enforcement/rate-limit` | Apply per-user transaction rate limits |
| `POST` | `/api/enforcement/invalidate-sessions` | Invalidate all active sessions for a user |
| `POST` | `/api/enforcement/notify-email` | Send incident notification email (async background task) |

### Supporting Routes

| Group | Endpoints |
|-------|-----------|
| **Beneficiarios** | CRUD for transfer destination accounts |
| **OTP Challenges** | Create / verify MFA challenges |
| **Sessions** | List / revoke user sessions |
| **Token Blacklist** | Add / check revoked JWT tokens |
| **Risk Assessments** | Read pipeline outputs per transaction |
| **Fraud Actions** | Read enforcement records |
| **Security Events** | Query auth event trail |
| **Audit Logs** | Query full API audit trail |
| **IP Reputation** | Read / upsert IP risk metadata |

Interactive docs are available at `/docs` (Swagger UI) and `/redoc` when the server is running.

---

## Agent Pipeline

The agent is a **SequentialAgent** (Google ADK) with three specialized LLM sub-agents. Each stage has a well-defined input/output contract enforced via `output_key` state passing.

### Agent State Machine

<img width="3585" height="629" alt="Agent state machine diagram showing the risk_engine → decision_engine → action_engine pipeline" src="https://github.com/user-attachments/assets/f4af7d5e-4639-46e7-8a2c-b6cbad6a521c" />

---

### Stage 1 — Risk Engine

**Input:** `TransactionEventRequest` (9 signal fields)  
**Output key:** `risk_assessment`  
**LLM:** Gemini 2.5 Flash  

Calls the 10 fraud-scoring tools and then calls `compute_aggregate_risk_score` to produce a final `0.0–1.0` score with a risk level label.

#### Scoring Tools

| Tool | Signal | Description |
|------|--------|-------------|
| `score_amount_deviation` | Amount | Z-score vs. user's historical mean/std |
| `score_velocity` | Velocity | Transaction count spike ratio vs. baseline |
| `score_device_trust` | Device | Known device age, trust status, fraud flags |
| `score_geolocation_anomaly` | Geolocation | Impossible-travel detection via Haversine distance |
| `score_new_beneficiaries` | Beneficiaries | Spike in new destination accounts |
| `score_account_takeover_signals` | ATO | Password/email/2FA changes + OTP failure count |
| `score_ip_network_risk` | IP | VPN, TOR, blacklist, provider risk score |
| `score_network_connectivity` | Network | Proximity to known-fraud accounts in transaction graph |
| `score_behavioral_deviation` | Behavior | Hour-of-day, channel, interaction pattern deviations |
| `compute_aggregate_risk_score` | Aggregate | Weighted average of all signals |

#### Signal Weights

| Signal | Weight |
|--------|--------|
| Geolocation | 15% |
| Account Takeover | 15% |
| Velocity | 12% |
| Device Trust | 12% |
| Amount Deviation | 10% |
| New Beneficiaries | 10% |
| IP Network Risk | 10% |
| Network Connectivity | 8% |
| Behavioral Deviation | 8% |

#### Risk Level Thresholds

| Level | Score Range |
|-------|-------------|
| `low` | < 0.30 |
| `medium` | 0.30 – 0.55 |
| `high` | 0.55 – 0.75 |
| `critical` | ≥ 0.75 |

---

### Stage 2 — Decision Engine

**Input:** `risk_assessment` from Stage 1  
**Output key:** `decision`  
**LLM:** Gemini 2.5 Flash  

Evaluates deterministic rules in priority order to produce a `verdict` (`approve`, `challenge`, `review`, `decline`) with an optional `freeze` flag and the matched rule ID.

#### Decision Rules

**HARD DECLINE — Fraud:**

| Rule ID | Condition |
|---------|-----------|
| `RULE_CRITICAL_SCORE` | `risk_score ≥ 0.75` |
| `RULE_ATO_CONFIRMED` | `account_takeover.score ≥ 0.80` |
| `RULE_FRAUD_NETWORK` | `network_connectivity.score ≥ 0.85` |
| `RULE_TOR_CRITICAL` | `ip_network_risk ≥ 0.90` AND `risk_score ≥ 0.50` |

**HUMAN REVIEW — Escalate:**

| Rule ID | Condition |
|---------|-----------|
| `RULE_HIGH_SCORE` | `risk_score` in `[0.55, 0.75)` |
| `RULE_VELOCITY_SPIKE` | `velocity.score ≥ 0.70` |
| `RULE_MULTI_SIGNAL_HIGH` | 3+ signals with `score ≥ 0.60` |

**CHALLENGE — Step-up Auth:**

| Rule ID | Condition | Method |
|---------|-----------|--------|
| `RULE_ATO_SUSPECTED` | `account_takeover.score` in `[0.30, 0.80)` | `otp_sms` |
| `RULE_NEW_DEVICE` | `device_trust.score ≥ 0.60` | `otp_sms` |
| `RULE_GEO_ANOMALY` | `geolocation_anomaly.score ≥ 0.65` | `otp_email` |
| `RULE_MEDIUM_SCORE` | `risk_score` in `[0.30, 0.55)` | `otp_sms` |
| `RULE_NEW_BENEFICIARIES` | `new_beneficiaries.score ≥ 0.60` | `otp_sms` |

**APPROVE:**

| Rule ID | Condition |
|---------|-----------|
| `RULE_LOW_SCORE` | `risk_score < 0.30` AND no signal `≥ 0.60` |

---

### Stage 3 — Action Engine

**Input:** `risk_assessment` + `decision`  
**Output key:** `action_result`  
**LLM:** Gemini 2.5 Flash  

Executes enforcement tools based on the decision verdict. Actions are non-reversible and logged in `FraudAction`.

#### Action Matrix

| Verdict | Freeze | Actions |
|---------|--------|---------|
| `approve` | — | None — `action_taken = "approved"` |
| `challenge` | — | Rate limit (3 txn / 30 min) · Send OTP email |
| `review` | — | Rate limit (1 txn / 60 min) · Escalation email |
| `decline` | No | Block account · Fraud notification email |
| `decline` | Yes | Block account · Invalidate sessions · Rate limit to 0 · Alert email |

#### Action Tools

| Tool | Description |
|------|-------------|
| `block_account` | Sets account status to `"blocked"` via enforcement API |
| `apply_transaction_rate_limit` | Enforces `max_transactions` within `window_minutes` |
| `invalidate_user_sessions` | Clears all active user sessions |
| `send_incident_email` | Async SMTP notification (Mailgun-compatible) |

---

## Frontend

A React 19 single-page application providing the operational dashboard.

**Key packages:** React Router 7 · Framer Motion · Lucide React · TypeScript 6

**Custom hooks:** `useRiskAction` · `useAuth` · `useMutation` · `useQuery` · `useToggle` · `useDebounce`

Run the dev server:

```bash
cd frontend
npm install
npm run dev
# http://localhost:3000
```

---

## Observability

The full observability stack (Prometheus, AlertManager, Grafana) starts automatically with Docker Compose and requires no manual setup.

### Metrics

The backend exposes a Prometheus-compatible `/metrics` endpoint via `prometheus-fastapi-instrumentator`. Three metric families are tracked per handler:

| Metric | Description |
|--------|-------------|
| `http_requests_total` | Request count, labelled by method, handler, and status code |
| `http_request_duration_seconds` | Latency histogram (p50 / p95 / p99) |
| `http_requests_in_progress` | In-flight request gauge |

Prometheus scrapes `/metrics` every **15 seconds** and retains data for **15 days**.

### Alerting

AlertManager routes firing alerts to email using the SMTP credentials from `.env`. Severity determines repeat interval:

| Alert | Condition | Severity | Repeat |
|-------|-----------|----------|--------|
| `ServiceDown` | Backend instance unreachable for > 1 min | critical | 1h |
| `HighErrorRate` | 5xx rate > 5% over 5 min | warning | 4h |
| `HighP95Latency` | p95 latency > 2s over 5 min | warning | 4h |
| `HighRequestRate` | Throughput > 500 req/s over 5 min | warning | 4h |

`warning` alerts are automatically suppressed when a `critical` alert with the same `alertname` is already firing (inhibition rule).

### Dashboards

The **Temis Overview** Grafana dashboard is auto-provisioned on container start. It provides four panels:

- **Request rate** — requests/sec split by 2xx / 4xx / 5xx
- **Latency percentiles** — p50, p95, p99 over time
- **Top handlers** — top-10 routes by throughput
- **Service status** — up/down stat panel

| Service | URL |
|---------|-----|
| Prometheus | `http://localhost:9090` |
| AlertManager | `http://localhost:9093` |
| Grafana | `http://localhost:3000` (default login: `admin` / `admin`) |

---

## Environment Variables

Copy `.env.example` to `.env` and fill in the required values.

```env
# General
ENVIRONMENT=development
LOG_LEVEL=info

# Frontend
FRONTEND_PORT=3000
FRONTEND_API_BASE_URL=http://localhost:8000

# Backend API
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
APP_NAME=Temis RiskControl API
APP_VERSION=0.1.0
DEBUG=false

# Agent Service
AGENT_HOST=0.0.0.0
AGENT_PORT=9000
AGENT_BACKEND_API_URL=http://localhost:8000

# LLM
GEMINI_API_KEY=<your-gemini-api-key>

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/temis_db
DATABASE_USERNAME=user
DATABASE_PASSWORD=password
DATABASE_NAME=temis_db

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Rate Limiting
RATE_LIMIT_ENABLED=true
BACKEND_RATE_LIMIT_WINDOW_SECONDS=60
BACKEND_RATE_LIMIT_MAX_REQUESTS=120
AGENT_RATE_LIMIT_WINDOW_SECONDS=60
AGENT_RATE_LIMIT_MAX_REQUESTS=30

# Email (SMTP / Mailgun)
SMTP_HOST=smtp.mailgun.org
SMTP_PORT=587
SMTP_USE_TLS=true
SMTP_USERNAME=<mailgun-username>
SMTP_PASSWORD=<mailgun-password>
SMTP_FROM_ADDRESS=noreply@temis.io

# Postgres (docker-compose)
POSTGRES_USER=temis
POSTGRES_PASSWORD=temis
POSTGRES_DB=temis_db

# Grafana
GRAFANA_ADMIN_USER=admin
GRAFANA_ADMIN_PASSWORD=admin

# AlertManager
ALERT_EMAIL_TO=ops@temis.io
```

---

## Getting Started

### Prerequisites

- Python 3.12+
- PostgreSQL (or SQLite for local dev)
- Node.js 18+
- Gemini API key
- Docker & Docker Compose (for the full observability stack)

### Full Stack (Docker Compose)

The fastest way to run everything — backend, agent, Postgres, Prometheus, AlertManager, and Grafana — in one command:

```bash
cp .env.example .env        # fill in GEMINI_API_KEY and SMTP credentials
docker compose up --build
```

| Service | URL |
|---------|-----|
| Backend API | `http://localhost:8000` |
| Agent Service | `http://localhost:8001` |
| Prometheus | `http://localhost:9090` |
| AlertManager | `http://localhost:9093` |
| Grafana | `http://localhost:3000` |

### Backend

```bash
# Clone and enter the repo
git clone https://github.com/<org>/temis-riskcontrol.git
cd temis-riskcontrol

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt

# Start the API server
export PYTHONPATH=backend
uvicorn app.main:app --reload --app-dir backend
# API   → http://localhost:8000
# Docs  → http://localhost:8000/docs
```

### Agent Service

```bash
cd agent
uvicorn risk_control_pipeline:app --host 0.0.0.0 --port 9000
# Agent → http://localhost:9000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
# UI → http://localhost:3000
```

---

## Running Tests

```bash
PYTHONPATH=backend pytest backend/tests -v
```

---

## CI/CD

The GitHub Actions workflow (`.github/workflows/ci.yml`) runs on every push and pull request:

1. **backend-python** — Dependency installation, compilation verification, FastAPI smoke test.
2. **backend-tests** — Full `pytest` suite with asyncio support.
3. **docker-build** — Validates the container image builds successfully.

---

## Diagrams

### Stack Diagram

<img width="2751" height="2017" alt="Stack diagram showing components and integration boundaries" src="https://github.com/user-attachments/assets/c7dee67a-3626-4b46-847c-ca3024b06e33" />

### Relational Model

<img width="2023" height="1776" alt="Relational model diagram showing core and supporting entities" src="https://github.com/user-attachments/assets/3cc397a9-a04a-4778-b6c6-49ab19f1c932" />

### Database Design Document

For the complete schema rationale, constraint definitions, and migration history see [`docs/database-design.pdf`](docs/database-design.pdf).

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
feat(agent): add geolocation scoring tool
fix(api): handle null response in webhook handler
docs(readme): update agent pipeline section
```

---
