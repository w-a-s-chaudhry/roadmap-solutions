# Todo List API

A full-stack todo app — FastAPI backend with JWT auth and a React +
TypeScript frontend.

Project page: https://roadmap.sh/projects/todo-list-api

## Architecture

```
Todo List API/
├── backend/          FastAPI + SQLAlchemy 2.x + SQLite
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── auth.py
│   │   ├── dependencies.py
│   │   ├── limiter.py
│   │   └── routers/
│   │       ├── users.py   /auth/register, /auth/login, /auth/refresh
│   │       └── todos.py   /todos CRUD
│   ├── tests/        16 tests, all passing
│   ├── pyproject.toml
│   └── uv.lock
└── frontend/         React + Vite + TypeScript + Tailwind v4
    ├── src/
    │   ├── api/api.ts             Axios instance + Bearer interceptor
    │   ├── context/AuthContext.tsx In-memory token store
    │   ├── pages/
    │   │   ├── LoginPage.tsx
    │   │   ├── RegisterPage.tsx
    │   │   └── TodosPage.tsx
    │   └── components/ui/         shadcn/ui components
    └── package.json
```

## Backend setup

Requires [uv](https://github.com/astral-sh/uv) (`pip install uv`).

```bash
cd "Todo List API/backend"
uv sync
cp .env.example .env   # set SECRET_KEY to any long random string
uv run uvicorn app.main:app --reload
```

Interactive API docs: http://localhost:8000/docs

### Run tests

```bash
uv run pytest
```

## Frontend setup

```bash
cd "Todo List API/frontend"
npm install
npm run dev
```

Open http://localhost:5173

## Features

- JWT access + refresh tokens; tokens stored in memory (not
  localStorage) for XSS safety
- Rate limiting on all auth endpoints (slowapi)
- Per-user todo isolation with ownership enforced at the DB layer
- Filter by done/priority, sort, paginate
- React frontend with TanStack Query for instant optimistic updates
