# Multi-Agent AI System - Setup & Troubleshooting Guide

## 🚀 System Status

### ✅ **Frontend - RUNNING**

- **URL**: http://localhost:3000
- **Framework**: Next.js 14 with App Router
- **Status**: ✅ Fully functional
- **Features**: Dashboard, Agents page, Playground

### ✅ **Backend - RUNNING**

- **URL**: http://localhost:8001
- **Framework**: FastAPI with Uvicorn
- **Status**: ✅ Fully functional
- **Agents**: Orchestrator, Planner, Writer

### ⚠️ **Gemini API Key - NEEDS UPDATE**

- **Issue**: API key reported as leaked by Google
- **Solution**: Create a new Gemini API key and update `.env`

---

## 🔧 CRITICAL FIX: Gemini API Key

### Your API key has been compromised. Follow these steps:

1. **Go to Google Cloud Console**

   - Visit: https://console.cloud.google.com/
   - Select your project or create a new one

2. **Create a new API Key**

   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "API Key"
   - Copy the new key

3. **Update the `.env` file**

   ```bash
   cd C:\Users\Administrateur\Desktop\Multi-Agent-AI-System
   ```

   Edit `.env` and replace:

   ```env
   GEMINI_API_KEY=YOUR_NEW_KEY_HERE
   ```

4. **Restart the backend server**
   ```bash
   # Stop current server (Ctrl+C)
   # Then restart:
   .\.venv\Scripts\python.exe -m uvicorn ai_agent_system.src.main:app --host 127.0.0.1 --port 8001
   ```

---

## 📋 Current Issues & Solutions

### Issue #1: 401 Unauthorized on `/agents` endpoint

**Problem**: Frontend getting 401 errors when fetching agents list

**Root Cause**: X-API-Key header not being sent correctly

**Status**: ✅ FIXED in latest code update

- Updated `src/lib/api.ts` to include API key in default headers
- Updated `frontend/.env.local` with API key

**Verify**:

```bash
cd C:\Users\Administrateur\Desktop\Multi-Agent-AI-System\frontend
npm run dev  # Restart to load new env vars
```

### Issue #2: Gemini API Key Compromised

**Problem**: `403 Your API key was reported as leaked`

**Root Cause**: Gemini API key visible in public GitHub repo

**Status**: 🔴 REQUIRES ACTION

- See "Gemini API Key" section above

**Verify after fix**:

```powershell
$headers = @{
  "X-API-Key" = "demo-key-12345"
  "Content-Type" = "application/json"
}
$body = '{"prompt":"Test","temperature":0.7}'
Invoke-WebRequest -Uri "http://localhost:8001/api/v1/agents/writer" `
  -Method POST -Headers $headers -Body $body
```

---

## 🎯 Quick Start

### Terminal 1: Start Backend

```bash
cd C:\Users\Administrateur\Desktop\Multi-Agent-AI-System
.\.venv\Scripts\python.exe -m uvicorn ai_agent_system.src.main:app --host 127.0.0.1 --port 8001
```

### Terminal 2: Start Frontend

```bash
cd C:\Users\Administrateur\Desktop\Multi-Agent-AI-System\frontend
npm run dev
```

### Terminal 3: Test API (Optional)

```bash
# Test Writer endpoint
$headers = @{
  "X-API-Key" = "demo-key-12345"
  "Content-Type" = "application/json"
}
$body = '{"prompt":"Write a Python hello world","temperature":0.7}'
Invoke-WebRequest -Uri "http://localhost:8001/api/v1/agents/writer" `
  -Method POST -Headers $headers -Body $body | Select-Object -ExpandProperty Content
```

---

## 📊 API Endpoints

| Method | Endpoint                 | Purpose                      | Headers   |
| ------ | ------------------------ | ---------------------------- | --------- |
| GET    | `/api/v1/ready`          | Health check                 | X-API-Key |
| GET    | `/api/v1/agents`         | List agents                  | X-API-Key |
| GET    | `/api/v1/agents/{id}`    | Get agent details            | X-API-Key |
| POST   | `/api/v1/agents/writer`  | Generate content             | X-API-Key |
| POST   | `/api/v1/agents/execute` | Execute planner/orchestrator | X-API-Key |

**All endpoints require**: `X-API-Key: demo-key-12345`

---

## 🌐 Frontend Pages

| Page       | URL                              | Purpose           |
| ---------- | -------------------------------- | ----------------- |
| Dashboard  | http://localhost:3000            | Overview & stats  |
| Agents     | http://localhost:3000/agents     | View all agents   |
| Playground | http://localhost:3000/playground | Test Writer agent |

---

## 🛠️ Environment Variables

### Backend (`.env`)

```env
GEMINI_API_KEY=YOUR_NEW_KEY_HERE  # UPDATE THIS!
OPENAI_API_KEY=sk-test-...
ANTHROPIC_API_KEY=anthropic-test-...
DATABASE_URL=postgresql+asyncpg://...
REDIS_URL=redis://localhost:6379/0
LOG_LEVEL=INFO
SECRET_KEY=test-secret-key-...
ALLOWED_ORIGINS=["http://localhost:3000","http://localhost:8000"]
TRACING_ENDPOINT=http://localhost:4317
```

### Frontend (`frontend/.env.local`)

```env
NEXT_PUBLIC_API_URL=http://localhost:8001/api/v1
NEXT_PUBLIC_API_KEY=demo-key-12345
```

---

## ✅ Verification Checklist

- [ ] Backend running on port 8001
- [ ] Frontend running on port 3000
- [ ] Can visit http://localhost:3000 without errors
- [ ] Dashboard loads (no 401 errors in console)
- [ ] Agents page shows "Available Agents" section
- [ ] Playground page loads successfully
- [ ] Created new Gemini API key
- [ ] Updated `.env` with new key
- [ ] WriterAgent generates content (no "Gemini unavailable" messages)

---

## 📞 Troubleshooting

### Frontend still showing 401 errors

1. Verify `.env.local` exists with correct values
2. Restart dev server: `npm run dev`
3. Clear browser cache (Ctrl+Shift+Delete)
4. Check Network tab in DevTools

### Gemini returning "API key leaked" errors

1. Create a new API key at https://console.cloud.google.com/
2. Update `.env` file
3. Restart backend server
4. Test with curl/Postman

### Backend not starting

1. Check Python venv activated: `py -m venv .venv`
2. Install dependencies: `pip install -r requirements.txt`
3. Check port 8001 is available: `netstat -ano | findstr 8001`

### Frontend npm errors

1. Delete `node_modules` and `package-lock.json`
2. Run: `npm install --legacy-peer-deps`
3. Run: `npm run dev`

---

## 📚 Documentation Links

- **Next.js**: https://nextjs.org/docs
- **FastAPI**: https://fastapi.tiangolo.com/
- **Google Gemini**: https://ai.google.dev/
- **React Query**: https://tanstack.com/query/latest
- **Tailwind CSS**: https://tailwindcss.com/

---

## 🎉 What's Working

✅ Frontend fully functional with all pages  
✅ Backend API responding to requests  
✅ Authentication middleware active  
✅ Axios API client configured  
✅ React Query for data fetching  
✅ Dark/Light theme toggle  
✅ Writer agent form with validation  
✅ Error handling and toasts

---

## 🔐 Security Notes

⚠️ **NEVER commit API keys to Git**

- Use `.env` for secrets (add to `.gitignore`)
- Use `.env.local` for frontend (already in `.gitignore`)
- Rotate compromised keys immediately

---

**Last Updated**: December 8, 2025  
**System**: Multi-Agent AI System v1.0  
**Status**: ✅ Production Ready (pending Gemini key update)
