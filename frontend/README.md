# Multi-Agent AI System - Next.js Frontend

Modern, production-ready Next.js 14 frontend for the Multi-Agent AI System.

## 🎯 Features

- **Next.js 14** with App Router
- **TypeScript** (strict mode)
- **Tailwind CSS** + dark/light mode
- **shadcn/ui** components
- **React Query** for data fetching
- **React Hook Form** + Zod validation
- **Axios** API client
- **Lucide React** icons
- **Sonner** toast notifications
- **Vercel Analytics** ready

## 🚀 Quick Start

```bash
# Install dependencies
npm install

# Start dev server
npm run dev

# Open http://localhost:3000
```

## 📁 Project Structure

```
src/
├── app/                    # Next.js App Router
│   ├── (layout)/          # Main layout with header
│   │   ├── page.tsx       # Dashboard
│   │   ├── agents/        # Agents page
│   │   └── playground/    # Playground page
│   ├── layout.tsx         # Root layout
│   └── globals.css        # Global styles
├── components/
│   ├── ui/                # shadcn/ui components
│   ├── header.tsx         # Navigation header
│   ├── writer-card.tsx    # Writer agent form
│   ├── agents-list.tsx    # Agents display
│   ├── theme-provider.tsx
│   └── query-provider.tsx
├── hooks/
│   └── use-agents.ts      # React Query hooks
├── types/
│   └── api.ts             # TypeScript types
└── lib/
    ├── api.ts             # Axios instance
    ├── utils.ts           # Helper functions
    └── site.ts            # Site config
```

## 🔌 API Integration

The frontend connects to the Python FastAPI backend at `http://localhost:8001/api/v1`.

### Environment Variables

Create `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8001/api/v1
```

### Available Endpoints

- **GET** `/agents` - List all agents
- **GET** `/agents/{agent_id}` - Get agent details
- **POST** `/agents/writer` - Generate content with WriterAgent
- **POST** `/agents/execute` - Execute Planner/Orchestrator

## 🎨 Styling & Theming

- Tailwind CSS for all styling
- `next-themes` for dark/light mode toggle
- CSS variables for color system
- Responsive design (mobile-first)

## 🧪 Component Examples

### WriterCard Component

Form for generating content with the Gemini-powered WriterAgent:

```tsx
<WriterCard />
```

### AgentsList Component

Display available agents and their capabilities:

```tsx
<AgentsList />
```

## 📦 Dependencies

### Core
- `next` 14.2.12
- `react` 18.3.1
- `typescript` 5.6.3

### UI & Styling
- `tailwindcss` 3.4.13
- `shadcn/ui` (via radix-ui primitives)
- `lucide-react` 0.469.0

### Data & Forms
- `@tanstack/react-query` 5.59.0
- `react-hook-form` 7.52.1
- `zod` 3.23.8

### Utils
- `axios` 1.7.7
- `next-themes` 0.3.0
- `date-fns` 3.6.0
- `sonner` 1.5.0

## 🚀 Deployment

### Vercel (Recommended)

```bash
vercel
```

### Docker

```bash
docker build -t multi-agent-frontend .
docker run -p 3000:3000 multi-agent-frontend
```

### Environment Variables for Production

```env
NEXT_PUBLIC_API_URL=https://your-backend-url/api/v1
```

## 📊 Analytics

Vercel Analytics is integrated:

```tsx
import { Analytics } from "@vercel/analytics/react";
```

## 🔐 Security

- API key sent via `X-API-Key` header
- CORS configured on backend
- Input validation with Zod
- Environment variables for sensitive data

## 🎯 Next Steps

- Add authentication/login
- Implement agent history
- Add streaming responses
- Create custom hooks for each agent
- Add PWA support
- Implement error boundaries

## 📝 License

MIT
