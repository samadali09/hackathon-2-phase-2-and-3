# Phase II Specifications - Overview

## Purpose

Phase II transforms the console todo app into a **full-stack web application** with multi-user support, authentication, and persistent storage.

---

## Evolution from Phase I

| Aspect | Phase I | Phase II |
|--------|---------|----------|
| **Interface** | Console (CLI) | Web (Browser) |
| **Storage** | In-memory | PostgreSQL (Neon) |
| **Users** | Single-user | Multi-user with auth |
| **Deployment** | Local only | Cloud (Vercel + Railway/Render) |
| **Architecture** | Monolithic | Client-Server (REST API) |

---

## Technology Stack

### Frontend
- **Framework**: Next.js 16 (App Router)
- **Language**: TypeScript
- **Styling**: Vanilla CSS
- **Authentication**: Better Auth (client-side)
- **Deployment**: Vercel

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.13+
- **ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: JWT verification
- **Deployment**: Railway or Render

### Authentication
- **Provider**: Better Auth
- **Method**: JWT tokens
- **Flow**: Frontend generates JWT → Backend verifies JWT
- **Shared Secret**: `BETTER_AUTH_SECRET` environment variable

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Browser                              │
│  ┌────────────────────────────────────────────────────┐     │
│  │           Next.js Frontend (Vercel)                │     │
│  │  ┌──────────────┐  ┌──────────────┐               │     │
│  │  │ Auth Pages   │  │  Dashboard   │               │     │
│  │  │ (Sign In/Up) │  │  (Tasks)     │               │     │
│  │  └──────────────┘  └──────────────┘               │     │
│  │         │                  │                       │     │
│  │         └──────────────────┘                       │     │
│  │                │                                    │     │
│  │         Better Auth (JWT)                          │     │
│  └────────────────┼───────────────────────────────────┘     │
└──────────────────┼────────────────────────────────────────┘
                   │ HTTP + JWT Token
                   ▼
┌─────────────────────────────────────────────────────────────┐
│              FastAPI Backend (Railway/Render)               │
│  ┌────────────────────────────────────────────────────┐     │
│  │  JWT Middleware → Verify Token → Extract user_id  │     │
│  └────────────────┬───────────────────────────────────┘     │
│                   │                                          │
│  ┌────────────────▼───────────────────────────────────┐     │
│  │           REST API Endpoints                       │     │
│  │  GET/POST/PUT/DELETE /api/{user_id}/tasks         │     │
│  └────────────────┬───────────────────────────────────┘     │
│                   │                                          │
│  ┌────────────────▼───────────────────────────────────┐     │
│  │              SQLModel ORM                          │     │
│  └────────────────┬───────────────────────────────────┘     │
└──────────────────┼────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│           Neon PostgreSQL Database                          │
│  ┌──────────────┐  ┌──────────────┐                        │
│  │ users table  │  │ tasks table  │                        │
│  │ (Better Auth)│  │ (user_id FK) │                        │
│  └──────────────┘  └──────────────┘                        │
└─────────────────────────────────────────────────────────────┘
```

---

## Key Features

### 1. User Authentication
- Sign up with email and password
- Sign in to access tasks
- JWT tokens for API authentication
- Automatic token refresh

### 2. Multi-User Support
- Each user has their own tasks
- User isolation enforced at database level
- API endpoints filter by user_id

### 3. Persistent Storage
- Tasks saved to PostgreSQL database
- Data survives server restarts
- Automatic timestamps (created_at, updated_at)

### 4. Web Interface
- Modern, responsive design
- Works on desktop and mobile
- Intuitive task management
- Real-time updates

### 5. Cloud Deployment
- Frontend on Vercel (global CDN)
- Backend on Railway/Render (scalable)
- Database on Neon (serverless PostgreSQL)

---

## User Flows

### Sign Up Flow
1. User visits landing page
2. Clicks "Sign Up"
3. Enters email and password
4. Better Auth creates account
5. JWT token generated
6. Redirected to dashboard

### Sign In Flow
1. User visits landing page
2. Clicks "Sign In"
3. Enters credentials
4. Better Auth validates
5. JWT token generated
6. Redirected to dashboard

### Task Management Flow
1. User authenticated (has JWT)
2. Dashboard loads tasks via API
3. API verifies JWT, extracts user_id
4. Database query filtered by user_id
5. Tasks displayed in UI
6. User performs CRUD operations
7. Each operation sends JWT with request
8. Backend enforces user isolation

---

## Security

### Authentication
- Passwords hashed by Better Auth
- JWT tokens expire after 7 days
- Tokens stored in httpOnly cookies
- HTTPS in production

### Authorization
- Every API request requires valid JWT
- Backend verifies JWT signature
- user_id extracted from token
- Database queries filtered by user_id

### Data Isolation
- Users can only see their own tasks
- API endpoints enforce user_id matching
- Database indexes for performance

---

## Data Model

### Users Table (Better Auth)
```sql
CREATE TABLE users (
    id TEXT PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    name TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Tasks Table
```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(id),
    title VARCHAR(200) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_completed ON tasks(completed);
```

---

## API Endpoints

All endpoints require JWT authentication.

### List Tasks
```
GET /api/{user_id}/tasks
Authorization: Bearer <jwt_token>

Response: Array of Task objects
```

### Create Task
```
POST /api/{user_id}/tasks
Authorization: Bearer <jwt_token>
Body: { "title": "...", "description": "..." }

Response: Created Task object
```

### Get Task
```
GET /api/{user_id}/tasks/{task_id}
Authorization: Bearer <jwt_token>

Response: Task object
```

### Update Task
```
PUT /api/{user_id}/tasks/{task_id}
Authorization: Bearer <jwt_token>
Body: { "title": "...", "description": "..." }

Response: Updated Task object
```

### Delete Task
```
DELETE /api/{user_id}/tasks/{task_id}
Authorization: Bearer <jwt_token>

Response: 204 No Content
```

### Toggle Completion
```
PATCH /api/{user_id}/tasks/{task_id}/complete
Authorization: Bearer <jwt_token>

Response: Updated Task object
```

---

## Environment Variables

### Frontend (.env.local)
```
NEXT_PUBLIC_APP_URL=http://localhost:3000
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=<your-secret-here>
```

### Backend (.env)
```
DATABASE_URL=postgresql://user:pass@host.neon.tech/db
BETTER_AUTH_SECRET=<same-secret-as-frontend>
CORS_ORIGINS=http://localhost:3000,https://your-app.vercel.app
```

---

## Development Workflow

### Local Development
1. Start backend: `cd backend && uvicorn main:app --reload`
2. Start frontend: `cd frontend && npm run dev`
3. Access app: http://localhost:3000
4. API docs: http://localhost:8000/docs

### Testing
1. Sign up a new user
2. Create tasks
3. Update tasks
4. Mark complete
5. Delete tasks
6. Sign out and sign in again
7. Verify tasks persist

---

## Deployment

### Frontend (Vercel)
1. Connect GitHub repository
2. Select `frontend` folder as root
3. Add environment variables
4. Deploy

### Backend (Railway/Render)
1. Connect GitHub repository
2. Select `backend` folder as root
3. Add environment variables
4. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Deploy

### Database (Neon)
1. Create project
2. Create database
3. Copy connection string
4. Add to backend environment variables

---

## Success Criteria

Phase II is complete when:

- ✅ Users can sign up and sign in
- ✅ JWT authentication works
- ✅ All 5 CRUD operations work via web UI
- ✅ User isolation enforced (users only see their tasks)
- ✅ Data persists in database
- ✅ Frontend deployed to Vercel
- ✅ Backend deployed to Railway/Render
- ✅ Responsive design works on mobile
- ✅ Production environment fully functional

---

## Migration from Phase I

### Reused Concepts
- Task data model (same fields)
- Validation rules (title, description lengths)
- Business logic patterns

### New Additions
- User authentication
- Multi-user support
- Database persistence
- REST API
- Web UI
- Cloud deployment

---

## Next Steps

1. Set up Neon database
2. Create backend FastAPI project
3. Create frontend Next.js project
4. Implement authentication
5. Build API endpoints
6. Build UI components
7. Test locally
8. Deploy to production
9. Submit Phase II
