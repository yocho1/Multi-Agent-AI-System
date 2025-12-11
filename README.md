# Multi-Agent AI System

Production-ready multi-agent AI platform built with FastAPI, Next.js, Firebase, and Google Gemini. Specialized agents (orchestrator, planner, writer, weather) collaborate with real-time data integration, authentication, and caching.

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- Node.js 18+
- Firebase project (see [Firebase Setup Guide](./FIREBASE_SETUP.md))

### Backend Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your Firebase credentials and API keys

# Run backend
.\.venv\Scripts\python.exe -m uvicorn ai_agent_system.src.main:app --host 127.0.0.1 --port 8001 --reload
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.local.example .env.local
# Edit .env.local with your Firebase config

# Run frontend
npm run dev
```

Visit `http://localhost:3001` to access the application.

## 🔥 Features

### Authentication & Security

- **Firebase Authentication**: Email/password and Google Sign-In
- **JWT Token Verification**: Secure API endpoints with Firebase tokens
- **Protected Routes**: Authentication middleware for sensitive operations

### AI Agents

- **Orchestrator Agent**: Coordinates multiple agents for complex tasks
- **Planner Agent**: Breaks down tasks into actionable steps
- **Writer Agent**: Content generation powered by Google Gemini 2.5-flash
- **Weather Agent**: Real-time weather data from Open-Meteo API

### Caching & Performance

- **Firestore Caching**: Replaces Redis with Firebase Firestore
- **Automatic TTL**: Cache expiration for agent responses
- **JSON Support**: Structured data caching

### Modern UI

- **Next.js 14**: App Router with React Server Components
- **Tailwind CSS**: Modern, responsive design
- **shadcn/ui**: Accessible component library
- **Dark/Light Mode**: Theme switching support

## 📁 Project Structure

```
Multi-Agent-AI-System/
├── ai_agent_system/          # Backend (FastAPI)
│   └── src/
│       ├── agents/           # AI agent implementations
│       ├── api/              # API endpoints and middleware
│       │   ├── endpoints/    # Auth and agent endpoints
│       │   └── middleware/   # Authentication middleware
│       ├── config/           # Configuration and settings
│       └── utils/            # Firebase auth, cache, logging
├── frontend/                 # Frontend (Next.js)
│   └── src/
│       ├── app/              # Next.js pages
│       ├── components/       # React components
│       │   ├── auth/         # Login/Register forms
│       │   └── ui/           # shadcn/ui components
│       ├── contexts/         # Auth context provider
│       └── lib/              # Firebase configuration
├── .env                      # Backend environment variables
├── FIREBASE_SETUP.md         # Detailed Firebase setup guide
└── README.md                 # This file
```

## 🔧 Configuration

### Backend (.env)

```env
# AI API Keys
GEMINI_API_KEY=your_gemini_api_key

# Firebase Configuration
FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json

# Application Settings
LOG_LEVEL=INFO
SECRET_KEY=your-secret-key
ALLOWED_ORIGINS=["http://localhost:3001"]
```

### Frontend (.env.local)

```env
# Firebase Configuration
NEXT_PUBLIC_FIREBASE_API_KEY=your_api_key
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
NEXT_PUBLIC_FIREBASE_PROJECT_ID=your-project-id
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=your-project.appspot.com
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=your_sender_id
NEXT_PUBLIC_FIREBASE_APP_ID=your_app_id

# Backend API
NEXT_PUBLIC_API_URL=http://127.0.0.1:8001
```

## 📚 Documentation

- [Firebase Setup Guide](./FIREBASE_SETUP.md) - Complete Firebase configuration
- [API Documentation](http://127.0.0.1:8001/docs) - Interactive API docs (when backend is running)

## 🏗️ Architecture

### Tech Stack

- **Backend**: FastAPI, Python 3.12, Firebase Admin SDK
- **Frontend**: Next.js 14, React 18, TypeScript
- **AI**: Google Gemini 2.5-flash
- **Auth**: Firebase Authentication
- **Database**: Firebase Firestore (caching)
- **APIs**: Open-Meteo (weather data)

### Key Components

1. **Firebase Authentication**: Replaces Docker-based auth with managed service
2. **Firestore Caching**: Replaces Redis with Firebase Firestore
3. **Agent System**: Modular, extensible AI agent architecture
4. **REST API**: FastAPI with automatic OpenAPI documentation

## 🔐 Security

- **No Docker Required**: Simplified deployment without containers
- **Firebase Security**: Managed authentication and database security
- **Environment Variables**: Sensitive data stored securely
- **CORS Protection**: Configured allowed origins
- **Token Verification**: JWT validation on protected endpoints

## 🚢 Deployment

### Backend (Python)

- Deploy to Google Cloud Run, AWS Lambda, or any Python hosting
- Use environment variables for Firebase credentials
- Enable Application Default Credentials (ADC) for production

### Frontend (Next.js)

- Deploy to Vercel, Netlify, or Firebase Hosting
- Configure environment variables in hosting platform
- Enable preview deployments for testing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🆘 Support

For issues and questions:

- Check [Firebase Setup Guide](./FIREBASE_SETUP.md)
- Review API documentation at `/docs` endpoint
- Open an issue on GitHub
