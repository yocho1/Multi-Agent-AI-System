# Firebase Setup Guide

This guide will help you set up Firebase Authentication and Firestore for the Multi-Agent AI System, replacing Docker/Redis/PostgreSQL.

## Prerequisites

- A Google account
- Node.js and Python installed
- Firebase CLI (optional, but recommended)

## Step 1: Create a Firebase Project

1. Go to the [Firebase Console](https://console.firebase.google.com/)
2. Click "Add Project" or "Create a project"
3. Enter a project name (e.g., "multi-agent-ai-system")
4. Enable Google Analytics (optional)
5. Click "Create project"

## Step 2: Enable Firebase Authentication

1. In your Firebase project, click "Authentication" in the left sidebar
2. Click "Get started"
3. Enable the following sign-in methods:
   - **Email/Password**: Click "Email/Password" → Toggle "Enable" → Save
   - **Google**: Click "Google" → Toggle "Enable" → Save
4. (Optional) Configure authorized domains if deploying to production

## Step 3: Enable Cloud Firestore

1. In your Firebase project, click "Firestore Database" in the left sidebar
2. Click "Create database"
3. Select "Start in production mode" (you can adjust rules later)
4. Choose a Cloud Firestore location (select closest to your users)
5. Click "Enable"

### Configure Firestore Security Rules

Update your Firestore security rules to allow authenticated users to read/write cache:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Cache collection - authenticated users can read/write their own cache entries
    match /cache/{document=**} {
      allow read, write: if request.auth != null;
    }
  }
}
```

## Step 4: Get Firebase Configuration (Frontend)

1. In Firebase Console, click the gear icon ⚙️ → "Project settings"
2. Scroll down to "Your apps" section
3. Click the web icon `</>` to add a web app
4. Register app with a nickname (e.g., "AI Agent Frontend")
5. Copy the configuration object that looks like:

```javascript
const firebaseConfig = {
  apiKey: 'AIza...',
  authDomain: 'your-project.firebaseapp.com',
  projectId: 'your-project-id',
  storageBucket: 'your-project.appspot.com',
  messagingSenderId: '123456789',
  appId: '1:123456789:web:abc123',
}
```

6. Update `frontend/.env.local`:

```env
NEXT_PUBLIC_FIREBASE_API_KEY=AIza...
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
NEXT_PUBLIC_FIREBASE_PROJECT_ID=your-project-id
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=your-project.appspot.com
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=123456789
NEXT_PUBLIC_FIREBASE_APP_ID=1:123456789:web:abc123
NEXT_PUBLIC_API_URL=http://127.0.0.1:8001
```

## Step 5: Get Service Account Credentials (Backend)

1. In Firebase Console, click the gear icon ⚙️ → "Project settings"
2. Go to "Service accounts" tab
3. Click "Generate new private key"
4. Click "Generate key" in the dialog
5. A JSON file will be downloaded (e.g., `your-project-firebase-adminsdk-xxxxx.json`)
6. **IMPORTANT**: Keep this file secure! Never commit it to version control
7. Move this file to your project root and rename it to `firebase-credentials.json`

## Step 6: Configure Backend Environment

Update `.env` file in the project root:

```env
# Firebase Configuration (Backend)
FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json

# AI API Keys
GEMINI_API_KEY=your_gemini_api_key

# Application Settings
LOG_LEVEL=INFO
SECRET_KEY=your-production-secret-key
ALLOWED_ORIGINS=["http://localhost:3000","http://localhost:3001","http://localhost:8000"]
```

## Step 7: Install Dependencies

### Backend

```bash
cd ai_agent_system
pip install firebase-admin
```

### Frontend

```bash
cd frontend
npm install firebase
```

## Step 8: Run the Application

### Start Backend

```bash
# From project root
.\.venv\Scripts\python.exe -m uvicorn ai_agent_system.src.main:app --host 127.0.0.1 --port 8001 --reload
```

### Start Frontend

```bash
cd frontend
npm run dev
```

## Step 9: Test Authentication

1. Navigate to `http://localhost:3001/register`
2. Create a new account with email/password or Google
3. You should be redirected to the dashboard
4. Check Firebase Console → Authentication → Users to see your new user

## Security Best Practices

### 1. Protect Service Account Credentials

Add to `.gitignore`:

```
firebase-credentials.json
```

### 2. Use Environment Variables in Production

For production deployment:

- Use environment variables instead of files for credentials
- Use Firebase Admin SDK with Application Default Credentials (ADC)
- Never expose service account keys in client-side code

### 3. Configure Firestore Security Rules

Update security rules for production:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /cache/{cacheId} {
      // Only allow authenticated users to access cache
      allow read, write: if request.auth != null;

      // Prevent excessive writes (rate limiting)
      allow create: if request.auth != null &&
        request.time > resource.data.created_at + duration.value(1, 's');
    }
  }
}
```

### 4. Enable App Check (Optional but Recommended)

1. Go to Firebase Console → App Check
2. Enable App Check for your web app
3. Use reCAPTCHA or other provider
4. This helps prevent abuse and unauthorized access

## Firestore Caching

The system uses Firestore as a cache replacement for Redis with the following features:

- **Automatic TTL**: Cache entries expire automatically based on `expires_at` field
- **JSON Support**: `set_json()` and `get_json()` for complex objects
- **Agent Results Caching**: Agent execution results cached for 1 hour
- **Writer Agent Caching**: Content generation results cached for 1 hour

### Cache Key Structure

```
agent:{agent_id}:{md5_hash_of_task}
writer:{md5_hash_of_prompt_and_params}
```

## Authentication Flow

### Frontend → Backend

1. User logs in via Firebase Auth (frontend)
2. Frontend gets Firebase ID token
3. Frontend sends token in `Authorization: Bearer <token>` header
4. Backend verifies token using Firebase Admin SDK
5. Backend returns user info or protected resource

### Example API Call with Auth

```typescript
const token = await getIdToken()

const response = await fetch('http://127.0.0.1:8001/api/v1/auth/me', {
  headers: {
    Authorization: `Bearer ${token}`,
  },
})
```

## Troubleshooting

### "Invalid credentials" error

- Verify `FIREBASE_CREDENTIALS_PATH` points to correct file
- Check that service account JSON file is valid
- Ensure file permissions allow reading

### "Project not found" error

- Verify `projectId` matches in both frontend and backend configs
- Check Firebase Console that project is active

### CORS errors

- Ensure `ALLOWED_ORIGINS` in `.env` includes your frontend URL
- Check Firebase Auth authorized domains

### Cache not working

- Verify Firestore is enabled in Firebase Console
- Check Firestore security rules allow read/write
- Look for Firestore errors in backend logs

## Migration from Docker/Redis/PostgreSQL

The Firebase implementation provides:

✅ **Authentication**: Replaces custom JWT auth with Firebase Auth  
✅ **Caching**: Replaces Redis with Firestore  
✅ **No Docker**: No need for Docker containers  
✅ **Managed Service**: No server management required  
✅ **Scalability**: Auto-scales with Firebase

### What's Removed

- ❌ Docker containers for Redis/PostgreSQL
- ❌ Redis dependency
- ❌ PostgreSQL database (can still be added if needed)
- ❌ Manual user management

## Next Steps

- [ ] Set up Firebase Hosting for frontend deployment
- [ ] Configure Firebase Functions for serverless backend
- [ ] Set up Firebase Cloud Storage for file uploads
- [ ] Enable Firebase Analytics for usage tracking
- [ ] Configure backup and disaster recovery

## Resources

- [Firebase Documentation](https://firebase.google.com/docs)
- [Firebase Admin SDK Python](https://firebase.google.com/docs/admin/setup)
- [Firebase Web SDK](https://firebase.google.com/docs/web/setup)
- [Firestore Security Rules](https://firebase.google.com/docs/firestore/security/get-started)
