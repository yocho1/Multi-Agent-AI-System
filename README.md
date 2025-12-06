# Multi-Agent AI System

Production-ready multi-agent AI platform built with FastAPI, asyncio, and Clean Architecture. Specialized agents (orchestrator, planner, writer, flight, weather, code) collaborate via tools and workflows with observability and security baked in.

## Quick start

```bash
# Install poetry if needed
pip install --upgrade poetry

# Install dependencies
poetry install --no-root

# Run API locally
poetry run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## Project goals

- Modular, testable architecture (Clean Architecture, DI, repository pattern)
- Async-first stack (FastAPI, httpx, async SQLAlchemy)
- Observability from day 1 (structured logs, metrics, tracing)
- Security best practices (authn/z, rate limits, sandboxed code exec)
- Production deployment via Docker/Docker Compose

## Roadmap (phased)

- Week 1: settings/logging foundation, base agent/tool abstractions, FastAPI shell
- Week 2: orchestrator, planner, writer agents, tool registry, memory system
- Week 3: flight, weather, code, web-search, database agents
- Week 4: workflows (trip planning, code review, research), parallel engine
- Week 5: authn/z, rate limiting, monitoring/metrics, Docker deployment, hardening
