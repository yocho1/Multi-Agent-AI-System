# Redis & PostgreSQL Setup Guide

## Option 1: Using Docker (Recommended)

### Prerequisites

- Install Docker Desktop from https://www.docker.com/products/docker-desktop

### Steps

1. **Start the services:**

```powershell
cd C:\Users\Administrateur\Desktop\Multi-Agent-AI-System
docker-compose up -d
```

2. **Verify services are running:**

```powershell
docker-compose ps
```

You should see:

```
NAME                  STATUS
ai_agent_postgres     Up (healthy)
ai_agent_redis        Up (healthy)
```

3. **Test connections:**

```powershell
# Test PostgreSQL
docker-compose exec postgres psql -U postgres -d ai_agents -c "SELECT 1"

# Test Redis
docker-compose exec redis redis-cli ping
```

4. **View logs:**

```powershell
docker-compose logs -f
```

5. **Stop services:**

```powershell
docker-compose down
```

6. **Stop and remove data:**

```powershell
docker-compose down -v
```

---

## Option 2: Local Installation (Windows)

### PostgreSQL Installation

1. Download from https://www.postgresql.org/download/windows/
2. Run installer and follow prompts
3. Set password to `postgres` (matches .env)
4. Port: `5432` (default)
5. Create database: `ai_agents`

```powershell
# After installation, verify with psql
psql -U postgres -c "CREATE DATABASE ai_agents"
```

### Redis Installation

1. Download from https://github.com/microsoftarchive/redis/releases
2. Or use WSL2 with Redis:

```powershell
# In WSL2
sudo apt-get install redis-server
redis-cli ping  # Should return PONG
```

3. Or use Memurai (Windows native Redis):

```powershell
choco install memurai  # if using chocolatey
```

---

## Verify Configuration

Check `.env` file has correct connection strings:

```
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/ai_agents
REDIS_URL=redis://localhost:6379/0
```

---

## Run Server with Full Services

Once Redis and PostgreSQL are running:

```powershell
cd C:\Users\Administrateur\Desktop\Multi-Agent-AI-System
.venv\Scripts\python.exe -m uvicorn ai_agent_system.src.main:app --host 127.0.0.1 --port 8001
```

The app will now:

- ✅ Connect to PostgreSQL
- ✅ Connect to Redis
- ✅ Enable all features

---

## Troubleshooting

### "Connection refused" error

- Ensure Docker containers are running: `docker-compose ps`
- Or ensure local PostgreSQL/Redis services are running

### Database doesn't exist

```powershell
docker-compose exec postgres psql -U postgres -c "CREATE DATABASE ai_agents"
```

### Redis connection issues

```powershell
docker-compose logs redis
```

### Reset everything

```powershell
# Stop and remove containers and volumes
docker-compose down -v

# Restart fresh
docker-compose up -d
```

---

## Next Steps

Once services are running, the app will automatically:

1. Initialize database connections
2. Cache data in Redis
3. Store agent logs and history
4. Enable full API functionality

Health endpoint will show: `"status": "ok"`
