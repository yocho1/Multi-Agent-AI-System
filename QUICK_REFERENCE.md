# 🚀 Quick Reference Guide

## 5-Second Setup

```bash
# Terminal 1
cd C:\Users\Administrateur\Desktop\Multi-Agent-AI-System
.\.venv\Scripts\python.exe -m uvicorn ai_agent_system.src.main:app --host 127.0.0.1 --port 8001

# Terminal 2
cd C:\Users\Administrateur\Desktop\Multi-Agent-AI-System\frontend
npm run dev

# Browser
http://localhost:3000
```

---

## System URLs

| Component      | URL                              | Purpose                       |
| -------------- | -------------------------------- | ----------------------------- |
| Frontend       | http://localhost:3000            | Dashboard, Agents, Playground |
| Backend API    | http://localhost:8001            | FastAPI server                |
| API Docs       | http://localhost:8001/docs       | Swagger UI                    |
| Gemini Console | https://console.cloud.google.com | API keys                      |

---

## Key Files to Remember

| File                                      | Purpose           | Edit When            |
| ----------------------------------------- | ----------------- | -------------------- |
| `.env`                                    | Backend secrets   | Adding API keys      |
| `frontend/.env.local`                     | Frontend config   | Changing backend URL |
| `src/agents/specialized.py`               | WriterAgent logic | Modifying generation |
| `frontend/src/components/writer-card.tsx` | Writer form       | Changing UI          |

---

## Common Commands

```bash
# Start frontend dev server
cd frontend && npm run dev

# Build frontend
cd frontend && npm run build

# Start frontend production
cd frontend && npm start

# Lint frontend
cd frontend && npm run lint

# Start backend
.\.venv\Scripts\python.exe -m uvicorn ai_agent_system.src.main:app --host 127.0.0.1 --port 8001

# Format Python code
black src/

# Run Python tests
pytest

# Check Python imports
python -m mypy src/
```

---

## API Quick Reference

### Get Agents List

```bash
curl -H "X-API-Key: demo-key-12345" http://localhost:8001/api/v1/agents
```

### Generate Content

```bash
curl -X POST http://localhost:8001/api/v1/agents/writer \
  -H "X-API-Key: demo-key-12345" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Write hello world","temperature":0.7}'
```

### Health Check

```bash
curl http://localhost:8001/api/v1/ready
```

---

## Dependencies

### Frontend

- Install: `npm install --legacy-peer-deps`
- Update: `npm update`
- Clean: `npm install --legacy-peer-deps` (after deleting node_modules)

### Backend

- Install: `pip install -r requirements.txt`
- Update: `pip install --upgrade -r requirements.txt`

---

## Environment Variables

### CRITICAL - Update These

```env
# In .env file
GEMINI_API_KEY=YOUR_NEW_KEY_FROM_GOOGLE_CONSOLE
```

### Standard Values (Don't Change)

```env
# Backend
LOG_LEVEL=INFO
SECRET_KEY=test-secret-key-do-not-use-in-production-12345678901234567890

# Frontend (.env.local)
NEXT_PUBLIC_API_URL=http://localhost:8001/api/v1
NEXT_PUBLIC_API_KEY=demo-key-12345
```

---

## Troubleshooting Quick Fix

| Problem          | Fix                                                       |
| ---------------- | --------------------------------------------------------- |
| Port 3000 in use | Kill Node: `Get-Process node \| Stop-Process -Force`      |
| Port 8001 in use | Kill Python: `Get-Process python \| Stop-Process -Force`  |
| 401 errors       | Check `.env.local` has API key                            |
| 403 Gemini error | Update GEMINI_API_KEY in `.env`                           |
| npm ERR          | Delete node_modules, run `npm install --legacy-peer-deps` |
| Page blank       | Check browser console, restart npm                        |

---

## Important Notes

⚠️ **Never commit API keys to Git**

- Add to `.gitignore` ✅
- Use `.env` for secrets ✅
- Use environment variables on hosting ✅

✅ **Always test locally first**

- Frontend: http://localhost:3000
- Backend: http://localhost:8001
- Try all pages and forms

✅ **Update Gemini key immediately**

- Old key is compromised
- Get new one from Google Console
- Update `.env` and restart

---

## File Structure Quick Map

```
Frontend Components:
  src/app/(layout)/page.tsx          → Dashboard
  src/app/(layout)/agents/page.tsx   → Agents list
  src/app/(layout)/playground/       → Test area
  src/components/writer-card.tsx     → Writer form
  src/components/agents-list.tsx     → Agent display
  src/lib/api.ts                     → API client

Backend Endpoints:
  src/api/endpoints/agent_endpoints.py
    → GET /agents (list)
    → POST /agents/writer (generate)
    → POST /agents/execute (run)

Core Logic:
  src/agents/specialized.py          → WriterAgent
  src/tools/llm/gemini_client.py     → Gemini API
  src/config/settings.py             → Configuration
```

---

## Testing Workflow

1. **Start both servers** (see 5-Second Setup)
2. **Open http://localhost:3000**
3. **Navigate pages**:
   - Dashboard: Check stats display
   - Agents: Verify list loads
   - Playground: Test writer form
4. **Open DevTools** (F12)
   - Check Console for errors
   - Check Network for API calls
   - Verify 200 responses

---

## Deployment Checklist

- [ ] Update GEMINI_API_KEY
- [ ] Test locally fully
- [ ] `git add .` and `git commit`
- [ ] Set env vars on hosting platform
- [ ] Deploy frontend (Vercel)
- [ ] Deploy backend (Heroku/AWS)
- [ ] Test production URLs
- [ ] Monitor logs

---

## Support Documents

- 📖 **SETUP_GUIDE.md** - Complete setup & troubleshooting
- 🚀 **DEPLOYMENT.md** - Production deployment guide
- 📚 **README.md** - Project overview (root & frontend)
- 💻 **This File** - Quick reference

---

**Last Updated**: December 8, 2025  
**Status**: ✅ Ready to Use
