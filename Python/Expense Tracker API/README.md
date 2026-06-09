# Expense Tracker API

A full-stack expense tracking app — FastAPI backend with JWT auth and a
React + TypeScript frontend.

Project page: https://roadmap.sh/projects/expense-tracker-api

## Architecture

```
Expense Tracker API/
├── Backend/          FastAPI + SQLAlchemy 2.x + SQLite
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── auth.py
│   │   ├── dependencies.py
│   │   ├── limiter.py
│   │   └── routers/
│   │       ├── users.py     /auth/register, /auth/login,
│   │       │                /auth/refresh, /auth/me
│   │       └── expenses.py  /expenses CRUD + filtering + summary
│   └── tests/        26 tests, all passing
├── frontend/         React + Vite + TypeScript + Tailwind v4
│   └── src/
│       ├── api/api.ts              Axios instance + Bearer interceptor
│       ├── context/AuthContext.tsx In-memory token store
│       ├── pages/
│       │   ├── LoginPage.tsx
│       │   ├── RegisterPage.tsx
│       │   ├── DashboardPage.tsx
│       │   ├── ExpensesPage.tsx
│       │   ├── AddExpensePage.tsx
│       │   └── EditExpensePage.tsx
│       └── components/
│           ├── ExpenseForm.tsx     Shared Add/Edit form
│           └── ui/                shadcn/ui components
├── pyproject.toml
└── uv.lock
```

## Backend setup

Requires [uv](https://github.com/astral-sh/uv) (`pip install uv`).

```bash
cd "Expense Tracker API"
uv sync
cp .env.example .env   # set SECRET_KEY to any long random string
cd Backend
uv run uvicorn app.main:app --reload
```

Interactive API docs: http://localhost:8000/docs

### Run tests

```bash
cd "Expense Tracker API"
uv run pytest
```

## Frontend setup

```bash
cd "Expense Tracker API/frontend"
npm install
npm run dev
```

Open http://localhost:5173

## Features

- JWT access + refresh tokens; tokens stored in memory (not
  localStorage) for XSS safety
- Rate limiting on all auth endpoints (slowapi)
- Per-user expense isolation with ownership enforced at the DB layer
- Date-range filtering: past week, past month, last 3 months, custom
- Filter by category, sort by date or amount, paginate
- GET /expenses/summary — total spent, expense count, top category
- React frontend with TanStack Query; GBP currency throughout
