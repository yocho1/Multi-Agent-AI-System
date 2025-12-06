# Deployment Guide (placeholder)

- Build: `docker build -f docker/Dockerfile -t ai-agent-system .`
- Run: `docker compose -f docker/docker-compose.yml up --build`
- Env: configure .env with secrets, DB/Redis URLs, broker, tracing.
- Prod: set SECRET_KEY, tighten CORS, use managed Postgres/Redis/RabbitMQ.
