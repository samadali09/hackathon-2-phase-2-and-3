# Todo App - Phase II

A modern, full-stack todo application built for the "Evolution of Todo" Hackathon Phase II.

## 🎯 Overview

This is a production-ready todo application featuring:
- **Frontend**: Next.js 16 with TypeScript and Tailwind CSS v4
- **Backend**: Python FastAPI with SQLModel
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: JWT-based auth
- **UI/UX**: Enterprise-grade dark theme with micro-interactions

## ✨ Features

- ✅ **Full CRUD Operations**: Create, Read, Update, Delete tasks
- ✅ **Multi-user Support**: Each user has isolated task lists
- ✅ **Authentication**: Sign up and sign in with JWT tokens
- ✅ **Persistent Storage**: Tasks saved to PostgreSQL database
- ✅ **Real-time Stats**: Total, Active, and Completed task counts
- ✅ **Task Filters**: View All, Active, or Completed tasks
- ✅ **Premium UI**: Dark theme with smooth animations and hover effects
- ✅ **Responsive Design**: Works on all screen sizes

## 🏗️ Architecture

```
d:\Hackathon\
├── frontend/              # Next.js application
│   ├── app/
│   │   ├── page.tsx              # Landing page (auth)
│   │   ├── dashboard/page.tsx    # Main dashboard
│   │   ├── layout.tsx            # Root layout
│   │   └── globals.css           # Tailwind + animations
│   └── lib/
│       ├── api.ts                # API client
│       └── auth.ts               # Auth utilities
│
├── backend/               # FastAPI application
│   ├── main.py                   # App entry point
│   ├── models.py                 # SQLModel schemas
│   ├── database.py               # DB configuration
│   ├── auth.py                   # JWT middleware
│   └── routes.py                 # API endpoints
│
└── phase-1/               # Phase I console app
```

## 🚀 Getting Started

### Prerequisites

- Python 3.12+
- Node.js 18+
- PostgreSQL database (Neon account)

### Backend Setup

```powershell
cd backend

# Create virtual environment with Python 3.12
py -3.12 -m venv venv

# Activate virtual environment
. venv\Scripts\Activate.ps1

# Install dependencies
pip install --upgrade pip
pip install fastapi uvicorn[standard] sqlmodel python-jose[cryptography] python-dotenv pydantic psycopg2-binary

# Create .env file with your database URL
# DATABASE_URL=postgresql://...
# BETTER_AUTH_SECRET=your-secret-key

# Start backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

```powershell
cd frontend

# Install dependencies
npm install

# Create .env.local file
# NEXT_PUBLIC_API_URL=http://localhost:8000
# BETTER_AUTH_SECRET=your-secret-key

# Start frontend
npm run dev
```

### Access the Application

1. **Frontend**: http://localhost:3000
2. **Backend API**: http://localhost:8000
3. **API Docs**: http://localhost:8000/docs

## 📋 How to Use

1. **Sign Up**: Create an account with email and password
2. **Sign In**: Log in with your credentials
3. **Create Tasks**: Click "Add New Task" and fill in details
4. **Mark Complete**: Click the checkbox next to any task
5. **Edit Tasks**: Hover over a task and click the edit icon
6. **Delete Tasks**: Hover over a task and click the delete icon
7. **Filter Tasks**: Use All/Active/Completed buttons
8. **View Stats**: See total, active, and completed counts

## 🧪 Testing

See `HOW-TO-TEST.md` for complete testing instructions.

Quick test:
1. Sign up with `test@example.com` / `test123`
2. Create 3 tasks
3. Mark one complete
4. Test filters
5. Edit and delete tasks
6. Sign out and back in - tasks should persist!

## 🎨 Design Features

- **Dark Theme**: Professional #0A0A0A background
- **Gradient Accents**: Violet-to-blue brand colors
- **Micro-interactions**: Focus animations, hover effects
- **Smooth Transitions**: 150ms cubic-bezier easing
- **Icon Badges**: Visual clarity on stats
- **Staggered Animations**: Tasks fade in sequentially

## 🔧 Tech Stack

### Frontend
- Next.js 16 (App Router)
- TypeScript
- Tailwind CSS v4
- React Hooks

### Backend
- Python 3.12
- FastAPI
- SQLModel
- Uvicorn
- JWT Authentication

### Database
- Neon Serverless PostgreSQL
- SQLAlchemy ORM

## 📊 API Endpoints

- `GET /health` - Health check
- `GET /api/{user_id}/tasks` - List all tasks
- `POST /api/{user_id}/tasks` - Create task
- `GET /api/{user_id}/tasks/{task_id}` - Get task
- `PUT /api/{user_id}/tasks/{task_id}` - Update task
- `DELETE /api/{user_id}/tasks/{task_id}` - Delete task
- `PATCH /api/{user_id}/tasks/{task_id}/complete` - Toggle completion

## 🏆 Hackathon Requirements Met

### Phase II Requirements
- ✅ Full-stack web application
- ✅ Multi-user support with authentication
- ✅ Persistent storage (PostgreSQL)
- ✅ RESTful API
- ✅ Modern, responsive UI
- ✅ Task CRUD operations
- ✅ User isolation

### Bonus Features
- ✅ Enterprise-grade UI design
- ✅ Advanced micro-interactions
- ✅ Stats dashboard with completion %
- ✅ Task filters (All/Active/Completed)
- ✅ Real-time updates
- ✅ Professional dark theme

## 📝 Documentation

- `README.md` - This file
- `CLAUDE.md` - Claude Code integration details
- `constitution.md` - Project specifications
- `HOW-TO-TEST.md` - Complete testing guide

## 🐛 Troubleshooting

### Backend won't start
- Ensure Python 3.12 is installed
- Activate virtual environment
- Check DATABASE_URL in .env

### Frontend won't load
- Clear browser cache (Ctrl + Shift + Delete)
- Check backend is running on port 8000
- Verify .env.local file exists

### Authentication errors
- Clear browser localStorage
- Sign up with a new account
- Check JWT token format

## 🎉 Success!

Your Phase II Todo App is complete with:
- World-class enterprise UI
- Full CRUD functionality
- Multi-user support
- Persistent storage
- Professional polish

**Ready to present!** 🚀

## 📄 License

MIT License - Built for the Evolution of Todo Hackathon

## 👨‍💻 Author

Built with Claude Code for the Hackathon Phase II
