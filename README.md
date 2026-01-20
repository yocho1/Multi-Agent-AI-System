# Multi-Agent AI System

> **Production-grade multi-agent LLM orchestration platform** combining autonomous agent collaboration, real-time data integration, and enterprise-scale caching—designed for complex reasoning tasks at scale.

A sophisticated framework enabling specialized AI agents (orchestrator, planner, writer, weather) to coordinate asynchronously using FastAPI, Firebase infrastructure, and Google Gemini 2.5-flash for advanced reasoning and content generation.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Agents](#agents)
- [API Reference](#api-reference)
- [Configuration](#configuration)
- [Deployment](#deployment)
- [Contributing](#contributing)

---

## Overview

This system implements a **hierarchical multi-agent architecture** where specialized agents operate with distinct responsibilities:

- **Stateless design**: Agents operate independently; coordination handled by the orchestrator
- **Firebase-native**: Firestore for caching, Auth for identity, eliminates Redis/PostgreSQL dependency
- **Type-safe**: Full Pydantic validation, TypeScript frontend, mypy strict mode
- **Observability**: Structured logging, OpenTelemetry instrumentation, detailed request tracing

### Key Capabilities

| Feature                | Implementation                                                                       |
| ---------------------- | ------------------------------------------------------------------------------------ |
| **Agent Coordination** | Orchestrator agent routing requests to specialized agents (planner, writer, weather) |
| **LLM Integration**    | Google Gemini 2.5-flash with streaming support                                       |
| **Authentication**     | Firebase JWT validation, role-based access control                                   |
| **Caching Layer**      | Firestore TTL-based document caching for agent responses                             |
| **Real-time Data**     | Open-Meteo API for weather, extensible tool system                                   |
| **API Documentation**  | Auto-generated OpenAPI via FastAPI /docs endpoint                                    |

---

## Architecture

### System Design

```
┌─────────────────────────────────────────────────────────┐
│                   Next.js Frontend                       │
│         (React 18 + TypeScript + TailwindCSS)            │
└──────────────────────┬──────────────────────────────────┘
                       │ HTTPS/JWT Bearer
┌──────────────────────┴──────────────────────────────────┐
│                 FastAPI Backend (8001)                   │
├──────────────────────────────────────────────────────────┤
│ ┌─────────────────────────────────────────────────────┐ │
│ │           Request Pipeline                          │ │
│ │  [CORS] → [Auth] → [RateLimit] → [Logging]        │ │
│ └─────────────────────────────────────────────────────┘ │
├──────────────────────────────────────────────────────────┤
│ ┌───────────────────────────────────────────────────┐   │
│ │         Multi-Agent Orchestration Layer            │   │
│ │  ┌─────────────┬──────────────┬─────────────┐    │   │
│ │  │ Orchestrator│   Planner    │   Writer    │    │   │
│ │  │   Agent     │    Agent     │    Agent    │    │   │
│ │  └─────────────┴──────────────┴─────────────┘    │   │
│ │                       ↓                           │   │
│ │            ┌──────────────────────┐              │   │
│ │            │  Weather Agent       │              │   │
│ │            │  (Open-Meteo API)    │              │   │
│ │            └──────────────────────┘              │   │
│ └───────────────────────────────────────────────────┘   │
├──────────────────────────────────────────────────────────┤
│ ┌──────────────────┐  ┌──────────────────┐             │
│ │ Gemini API 2.5   │  │ Firestore Cache  │             │
│ │ (LLM Reasoning)  │  │ (TTL Expiry)     │             │
│ └──────────────────┘  └──────────────────┘             │
│         ↑                                               │
│ ┌──────────────────────────────────────┐              │
│ │  Firebase Admin SDK                   │              │
│ │  (Auth, Firestore, Credentials)      │              │
│ └──────────────────────────────────────┘              │
└──────────────────────────────────────────────────────────┘
```

### Technology Stack

| Layer                   | Technology    | Version    | Notes                              |
| ----------------------- | ------------- | ---------- | ---------------------------------- |
| **Backend**             | FastAPI       | 0.103+     | async-first, auto OpenAPI docs     |
| **Frontend**            | Next.js       | 14.2+      | App Router, RSC, server actions    |
| **Language (Backend)**  | Python        | 3.12+      | Type-safe with Pydantic v2         |
| **Language (Frontend)** | TypeScript    | 5.6+       | Strict mode enabled                |
| **Auth**                | Firebase Auth | SDK v7+    | Email/password, OAuth2 (Google)    |
| **Database**            | Firestore     | Native SDK | Document-oriented, real-time       |
| **LLM**                 | Google Gemini | 2.5-flash  | Multimodal, fast reasoning         |
| **External APIs**       | Open-Meteo    | Free       | Real-time weather, no key required |

### Project Structure

```
ai_agent_system/
├── src/
│   ├── agents/                    # Specialized agent implementations
│   │   ├── base/
│   │   │   ├── agent.py          # AbstractAgent base class
│   │   │   ├── memory.py         # Conversation memory & context
│   │   │   └── tool_registry.py  # Tool discovery & validation
│   │   ├── orchestrator.py       # Routing & coordination logic
│   │   ├── planner.py            # Task decomposition
│   │   ├── writer.py             # Content generation
│   │   └── weather.py            # Real-time weather queries
│   ├── api/
│   │   ├── endpoints/
│   │   │   ├── auth_endpoints.py       # Login, register, token refresh
│   │   │   ├── agent_endpoints.py      # Agent query endpoints
│   │   │   └── health_endpoints.py     # Liveness/readiness probes
│   │   └── middleware/
│   │       ├── auth_middleware.py      # JWT validation
│   │       ├── rate_limiter.py         # Sliding window rate limiting
│   │       └── request_logging.py      # Structured request/response logs
│   ├── config/
│   │   ├── settings.py           # Pydantic BaseSettings (env validation)
│   │   └── logging_config.py     # Structlog + loguru setup
│   ├── utils/
│   │   ├── firebase_auth.py      # Firebase Admin SDK wrapper
│   │   ├── firebase_cache.py     # Firestore TTL caching logic
│   │   ├── clients.py            # Singleton HTTP clients (aiohttp, etc)
│   │   ├── exceptions.py         # Custom exception hierarchy
│   │   ├── metrics.py            # Prometheus metrics
│   │   └── tracing.py            # OpenTelemetry instrumentation
│   └── main.py                    # FastAPI app initialization & lifespan
├── tests/
│   ├── unit/                     # Agent logic, cache, validators
│   ├── integration/              # End-to-end API tests
│   └── conftest.py               # Shared fixtures
├── pyproject.toml                 # Poetry dependencies (Python 3.12 compatible)
└── .env                           # Environment secrets (Firebase creds, API keys)

frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx             # Root layout, provider setup
│   │   ├── page.tsx               # Home landing page
│   │   ├── login/page.tsx         # Firebase auth form
│   │   └── (layout)/dashboard/    # Protected routes
│   ├── components/
│   │   ├── agents-list.tsx        # Agent selector & chat interface
│   │   ├── agent-showcase.tsx     # Interactive agent demos
│   │   └── ui/                    # shadcn/ui components
│   ├── contexts/
│   │   └── auth-context.tsx       # Firebase auth state (React Context)
│   ├── hooks/
│   │   ├── use-agents.ts          # SWR/React Query for agent calls
│   │   └── use-auth.ts            # Auth state hook
│   ├── lib/
│   │   ├── api.ts                 # Axios instance with token injection
│   │   └── firebase.ts            # Firebase client init
│   └── .env.local                 # Frontend env (NEXT_PUBLIC_*)
└── package.json                   # npm dependencies + scripts
```

---

## Quick Start

### Prerequisites

```bash
python --version  # >= 3.12
node --version    # >= 18
```

### Backend Setup

1. **Clone & navigate**:

   ```bash
   cd ai_agent_system
   ```

2. **Create virtual environment**:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # or: source .venv/bin/activate  # Unix
   ```

3. **Install dependencies**:

   ```bash
   pip install poetry
   poetry install --no-root
   ```

4. **Configure environment** (see [Configuration](#configuration)):

   ```bash
   cp .env.example .env
   # Edit .env with GEMINI_API_KEY and FIREBASE_CREDENTIALS_PATH
   ```

5. **Run server**:

   ```bash
   uvicorn ai_agent_system.src.main:app --host 127.0.0.1 --port 8001 --reload
   ```

   Server available at: `http://127.0.0.1:8001`  
   API docs: `http://127.0.0.1:8001/docs`

### Frontend Setup

1. **Navigate to frontend**:

   ```bash
   cd frontend
   ```

2. **Install dependencies**:

   ```bash
   npm install
   ```

3. **Configure environment**:

   ```bash
   cp .env.local.example .env.local
   # Edit with Firebase config values
   ```

4. **Run dev server**:

   ```bash
   PORT=3001 npm run dev
   ```

   Frontend available at: `http://localhost:3001`

---

## Agents

### Orchestrator Agent

Routes user queries to specialized agents based on intent classification.

**Inputs**: User query (string)  
**Outputs**: Delegated agent response + reasoning trace  
**LLM Calls**: 1–2 (routing + synthesis)

### Planner Agent

Decomposes complex tasks into ordered sub-tasks with dependencies.

**Inputs**: High-level goal  
**Outputs**: Step-by-step plan with resource requirements  
**LLM Calls**: 1+ (reasoning per level)

### Writer Agent

Generates coherent, well-structured content using in-context examples.

**Inputs**: Topic, tone, word count, style guidelines  
**Outputs**: Formatted document or article  
**LLM Calls**: 1–3 (draft → refinement → fact-check)

### Weather Agent

Queries Open-Meteo API for current & forecast weather data.

**Inputs**: Location (lat/lon or place name)  
**Outputs**: JSON weather object + human-readable summary  
**External API**: Open-Meteo (no authentication required)

---

## API Reference

### Base URL

```
http://127.0.0.1:8001/api/v1
```

### Authentication

All protected endpoints require Firebase ID token in `Authorization` header:

```http
Authorization: Bearer <firebase_id_token>
```

Obtain token via frontend auth context or direct Firebase SDK call.

### Key Endpoints

#### Health Checks

```http
GET /health
GET /ready
GET /metrics
```

#### Agent Queries

```http
POST /agents/orchestrator
Content-Type: application/json

{
  "query": "What's the weather in Paris and create a travel plan?",
  "session_id": "optional-uuid-for-context-retention"
}

Response:
{
  "agent": "orchestrator",
  "result": "...",
  "reasoning_trace": [...],
  "cached": false,
  "timestamp": "2026-01-20T20:15:28.328561Z"
}
```

```http
POST /agents/writer
Content-Type: application/json

{
  "prompt": "Write a technical blog post about multi-agent systems",
  "style": "technical, academic",
  "max_tokens": 2000
}
```

```http
POST /agents/planner
Content-Type: application/json

{
  "goal": "Deploy a production ML system in 30 days",
  "constraints": ["budget: $5k", "team size: 2"]
}
```

#### Full API docs

See interactive docs at `/docs` (Swagger UI) or `/redoc` (ReDoc)

---

## Configuration

### Backend Environment Variables

**Critical** (required for startup):

```env
GEMINI_API_KEY=AIzaSy...                    # Google AI Studio or Cloud Console
FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json  # Service account JSON
```

**Optional** (sensible defaults):

```env
LOG_LEVEL=INFO                              # DEBUG, INFO, WARNING, ERROR
SECRET_KEY=your-secret-key                  # For session signing
ALLOWED_ORIGINS=["http://localhost:3001"]   # CORS allow-list
TRACING_ENDPOINT=http://localhost:4317      # OpenTelemetry collector (optional)
```

**Deprecated** (not required with Firebase):

```env
# DATABASE_URL=postgresql://...             # Not needed
# REDIS_URL=redis://...                     # Not needed
```

### Frontend Environment Variables

**Required** (from Firebase Console):

```env
NEXT_PUBLIC_FIREBASE_API_KEY=AIzaSy...
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
NEXT_PUBLIC_FIREBASE_PROJECT_ID=your-project-id
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=your-project.appspot.com
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=236165915884
NEXT_PUBLIC_FIREBASE_APP_ID=1:236165915884:web:...
```

**Optional**:

```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8001  # Backend URL (default shown)
```

---

## Deployment

### Backend Deployment

**Google Cloud Run** (recommended):

```bash
gcloud run deploy multi-agent-backend \
  --source . \
  --platform managed \
  --region us-central1 \
  --set-env-vars GEMINI_API_KEY=$GEMINI_API_KEY,FIREBASE_CREDENTIALS_PATH=/secrets/firebase.json \
  --service-account-email <service-account-email>
```

**AWS Lambda** (with Mangum adapter):

```python
from mangum import Mangum
from ai_agent_system.src.main import app
handler = Mangum(app)
```

**Docker** (if needed):

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install poetry && poetry install --no-root
CMD ["uvicorn", "ai_agent_system.src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend Deployment

**Vercel** (native Next.js support):

```bash
vercel --prod
```

Environment variables configured in Vercel dashboard.

**Firebase Hosting**:

```bash
firebase deploy --only hosting
```

---

## Development

### Running Tests

```bash
# All tests
pytest ai_agent_system/src/tests -v

# Coverage report
pytest --cov=ai_agent_system.src ai_agent_system/src/tests

# Unit tests only
pytest ai_agent_system/src/tests/unit -v

# Integration tests (requires backend running)
pytest ai_agent_system/src/tests/integration -v
```

### Code Quality

```bash
# Format (Black)
black ai_agent_system/src

# Lint (Flake8)
flake8 ai_agent_system/src

# Type check (mypy, strict mode)
mypy --strict ai_agent_system/src
```

### Debugging

Enable debug logs:

```env
LOG_LEVEL=DEBUG
```

Check request/response tracing:

```bash
curl -v http://127.0.0.1:8001/api/v1/health
```

---

## Contributing

1. **Create feature branch**:

   ```bash
   git checkout -b feature/agent-enhancement
   ```

2. **Follow code standards**:
   - Type annotations required (mypy strict)
   - Tests for all new agents/utils
   - Docstrings for public APIs

3. **Run quality checks**:

   ```bash
   black . && flake8 . && mypy --strict . && pytest
   ```

4. **Open pull request** with clear description of changes

---

## License

MIT License – see [LICENSE](LICENSE) for details

---

## Support & Resources

- **API Docs**: http://127.0.0.1:8001/docs (Swagger)
- **Firebase Setup**: [FIREBASE_SETUP.md](./FIREBASE_SETUP.md)
- **Architecture Details**: [docs/architecture.md](./docs/architecture.md)
- **Deployment Guide**: [DEPLOYMENT.md](./DEPLOYMENT.md)
- **Issues**: Open GitHub issue with logs & environment details
