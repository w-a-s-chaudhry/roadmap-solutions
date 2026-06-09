Expense Tracker API — Handoff Notes

## Where you are
Last updated: 2026-06-09.
Previous project (Todo List API) is done; its handoff was archived to
F:\repos\roadmap-solutions\Python\Todo List API\HANDOFF.md.

### Backend — COMPLETE (B1–B6 ✅)
All production code and tests written and passing:
- B1 ✅ Scaffold: uv project, pyproject.toml, .env, main.py, database.py,
        auth.py, dependencies.py, limiter.py
- B2 ✅ User + auth router: register (with name), login, refresh tokens
- B3 ✅ Expense model, CategoryEnum (in models.py), all Pydantic schemas
- B4 ✅ Expense CRUD router with ownership enforcement
- B5 ✅ List filtering (category, sort, order, pagination),
        _resolve_range helper, GET /expenses/summary aggregation
- B6 ✅ 26 tests passing: auth (register/login/refresh/me) + CRUD +
        ownership-404 + filtering (range/category/custom/422) + summary

### Frontend — COMPLETE (F1–F7 ✅)
- F1 ✅ Scaffold: Vite+React+TS, Tailwind v4, shadcn components
        (button/card/input/label), api.ts, AuthContext, index.css,
        lib/utils.ts, App.tsx routing
- F2 ✅ LoginPage — fully implemented + styled to wireframe
- F2 ✅ RegisterPage — implemented (name + email + password + confirm)
- F3 ✅ AppLayout — sidebar, nav, user footer, logout, nested routes
- F4 ✅ DashboardPage — summary cards, range presets, recent expenses list,
        $0.00 amount formatting, navigate-to-edit on row click
- F5 ✅ AddExpensePage / EditExpensePage — shared ExpenseForm component,
        useMutation POST/PATCH/DELETE, query invalidation, navigate on success
- F6 ✅ ExpensesPage — queryFn with params, periodTotal, loading/error guards
- F7 ✅ Polish pass:
    - extractError in Add + Edit pages (typeof/Array.isArray pattern)
    - Dashboard loading/error guards
    - ExpensesPage: inline loading/error (filters stay visible on 422)

### Next action
Project is fully complete and clean — 26 tests passing, zero warnings
in our code. Archive this HANDOFF to
F:\repos\roadmap-solutions\Python\Expense Tracker API\HANDOFF.md
and move to the next roadmap.sh project.

## The project
roadmap.sh "Expense Tracker API" — https://roadmap.sh/projects/expense-tracker-api
The "last beginner backend project." Required: JWT auth (signup/login),
per-user CRUD on expenses, and date-range filtering (past week / past
month / last 3 months / custom). Fixed categories: Groceries, Leisure,
Electronics, Utilities, Clothing, Health, Others.

A wireframe ("Expensr") was supplied. Build the STANDARD scope:
Login, Register, Dashboard (overview cards + range filter + list),
Add/Edit expense, and the Filter/Expenses page.
OUT OF SCOPE (future / disabled nav): Summary charts page, Settings page.

Strategy: mirror the just-finished Todo List API (identical stack +
conventions). Copy its infrastructure modules; change only the domain
(Todo → Expense) and add date-range filtering, a category enum, money
handling, and a small summary endpoint.

## Collaboration mode: LEARNING MODE
- User writes all logic; Claude scaffolds skeletons with `# TODO`s,
  guides, and reviews (correctness + style/naming). User makes fixes.
- Each phase ends: walkthrough → quiz → gap-fill.
- New concepts → .jsx note under F:\Courses\roadmapsh\Python\.
- Toggle: /learning-mode | /professional-mode. Check: /current-mode

## Project locations (mirror Todo layout)
F:\repos\roadmap-solutions\Python\Expense Tracker API\
  ├── backend\   (FastAPI + SQLAlchemy + SQLite + JWT + slowapi, uv)
  └── frontend\  (React + Vite + TS + Tailwind v4 + shadcn + TanStack Query, npm)

Template to copy from:
  Backend:  F:\repos\roadmap-solutions\Python\Todo List API\backend\
  Frontend: F:\repos\roadmap-solutions\Python\Todo List API\frontend\

## Stack & conventions (unchanged from Todo)
Backend: FastAPI, SQLAlchemy 2.x, SQLite, Pydantic v2,
passlib+bcrypt(<5), python-jose, slowapi, python-dotenv, uv.
pytest with [tool.pytest.ini_options] pythonpath=["."].
Frontend: Vite, React 19, TS, Tailwind v4, shadcn (radix-nova),
TanStack Query, React Hook Form, Zod, axios, react-router-dom.
Style: file headers on every file (# Author: Wajid Ali Saleem Chaudhry /
# Description: ...), # --- Section --- headers, one-line # comment above
every def, no docstrings, <=80 columns. JS/TS uses the // equivalents.

## Domain design (the only real "new" thinking)

### Data model (backend/app/models.py)
- User — copy Todo's User, ADD `name = Column(String, nullable=False)`.
  Rename relationship to `expenses`.
- Expense — replaces Todo:
  - id
  - amount     = Column(Numeric(10, 2), nullable=False)
  - category   = Column(String, nullable=False, index=True)
  - description= Column(String, nullable=True)
  - date       = Column(Date, nullable=False, index=True)  # expense date
  - created_at / updated_at  (same func.now() pattern as Todo)
  - owner_id FK -> users.id, owner relationship
- Money: Numeric(10,2) <-> Pydantic Decimal, validated > 0.
  (Integer-cents is the production-grade alternative — course note only.)

### Category enum (backend/app/categories.py — new shared module)
class Category(str, Enum) with the 7 fixed values. Imported by schemas
(validation) and the router. Frontend keeps a matching hardcoded list.

### Schemas (backend/app/schemas.py)
- Add `name` to UserCreate and UserResponse.
- ExpenseCreate (amount, category: Category, date, description?),
  ExpenseUpdate (all optional), ExpenseResponse,
  PaginatedExpenses (mirror PaginatedTodos),
  ExpenseSummary (total_spent: Decimal, count: int, top_category: str|None).

### API surface (backend/app/routers/)
- users.py — copy Todo's auth router; register stores `name`.
  Add GET /auth/me (returns current UserResponse) for sidebar profile.
- expenses.py — copy Todo's todos.py shape:
  - POST /expenses, GET /expenses/{id}, PATCH /expenses/{id},
    DELETE /expenses/{id}  — CRUD + _get_owned_expense (ownership via 404)
  - GET /expenses — list with range filter + category filter +
    sort/order + pagination
  - GET /expenses/summary — aggregation for dashboard cards

### Filtering (the new endpoint logic)
- Helper _resolve_range(range, start_date, end_date) -> (start, end):
  past_week -> today-7d, past_month -> today-30d,
  last_3_months -> today-90d, custom -> requires both dates (422 if not).
- GET /expenses params: range (default past_month), start_date, end_date,
  category, sort=date, order=desc, page, size.
  Apply Expense.date >= start, <= end, optional category ==.
- GET /expenses/summary reuses _resolve_range; returns total_spent
  (func.sum), count (func.count), top_category
  (group_by(category).order_by(sum desc).first()).

### Infrastructure copied ~verbatim (rename todos.db -> expenses.db)
auth.py, dependencies.py, limiter.py, database.py, main.py (swap router
import + table-creation imports), .env, pyproject.toml, tests/conftest.py.

## Frontend screens (Standard scope)
Reuse Todo's api/api.ts, context/AuthContext.tsx, main.tsx, index.css,
lib/utils.ts, and shadcn button/card/input/label verbatim. Add shadcn
textarea and select (watch the @-folder quirk below). Category chips:
Button variants (no new dep). Dates: native <input type="date">
(deliberate simplification — avoids a date-picker dependency).

### Colour scheme (match the wireframe)
Override shadcn/Tailwind CSS variables in index.css to match Expensr:
- Background:   #F5F0E8  (warm beige — page + sidebar bg)
- Card/surface: #FFFFFF  (white cards, input fields)
- Primary:      #4A6FE3  (blue — buttons, active nav, selected chips)
- Primary-fg:   #FFFFFF  (white text on blue)
- Destructive:  #DC2626  (red — Delete button)
- Border:       #E2DAD0  (warm grey — card borders, dashed list dividers)
- Text:         #1A1A1A  (near-black)
- Muted text:   #6B7280  (category · date sublines, labels)
Apply during F1 alongside the rest of the CSS setup.

- LoginPage   — copy Todo's; posts JSON {email, password}.
- RegisterPage— copy Todo's; ADD `name` field + Zod rule.
- AppLayout   — new sidebar shell (logo; nav Dashboard / Expenses /
                Add expense; Summary + Settings rendered disabled "soon").
                User footer from GET /auth/me. Wraps private routes.
- DashboardPage — useQuery on /expenses/summary (3 cards: Spent / Top
                category / Count) + range preset buttons + useQuery on
                /expenses list rows (click row -> edit). "+ Add expense".
- ExpenseForm (shared Add/Edit) — amount, category chips, date,
                description. Add posts; Edit prefills (GET /expenses/{id}),
                Save (PATCH), Delete (destructive red), Discard.
                useMutation + query invalidation, pending/disabled states.
- ExpensesPage (filter/list) — range presets + custom start/end +
                category select + sort + "showing N · $total" + list.
- Routes: / Login, /register, then private /app (AppLayout) with
  /app Dashboard, /app/expenses, /app/expenses/new, /app/expenses/:id.

## Phased execution (learning mode — Claude scaffolds, user fills # TODOs)

BACKEND
- B1 — Scaffold: uv project, deps, copy auth/dependencies/limiter/
       database/main, .env, pyproject.toml. (Mechanical; Claude does it.)
- B2 — User + auth: add name; register/login/refresh/me. User writes
       register/login bodies.
- B3 — Expense model + Category enum + schemas. User writes columns/fields.
- B4 — Expense CRUD router (create/get/update/delete + ownership).
       User writes handlers off the Todo pattern.
- B5 — Filtering + summary: _resolve_range helper, GET /expenses filters,
       GET /expenses/summary aggregation. User writes query logic
       (new SQL aggregation concepts).
- B6 — Tests: auth + CRUD + filter + summary (target all passing).

FRONTEND
- F1 — Scaffold: copy config + api/auth/css; add textarea, select.
       (Mechanical; Claude does it.)
- F2 — Auth pages (Login + Register with name).
- F3 — AppLayout sidebar shell + /auth/me profile + routing.
- F4 — Dashboard (summary cards + range presets + list).
- F5 — ExpenseForm (Add + Edit + Delete).
- F6 — ExpensesPage (filters + totals + list).
- F7 — Polish (pending/disabled, inline errors, empty states).

Each phase: skeleton with # TODOs -> user implements -> Claude reviews
-> walkthrough -> quiz -> gap-fill.

## New concepts -> course notes (F:\Courses\roadmapsh\Python\)
- Money handling: Numeric/Decimal vs integer-cents (-> SQLAlchemy/).
- Shared str,Enum validation across ORM + Pydantic (-> FastAPI/).
- Date-range filtering + SQL aggregation (func.sum, group_by,
  order_by(... desc)) (-> SQLAlchemy/).
- Frontend app-shell layout + nested routes; derived/summary fetching;
  native date inputs (-> new React subfolder note).

## Known quirks to carry forward (from Todo)
- /auth/login expects JSON, NOT OAuth2 form data.
- api.ts interceptor header must use backticks: `Bearer ${_token}`.
- AuthContext imports setToken from '@/api/api' (path alias).
- import type { ReactNode } from 'react' (verbatimModuleSyntax).
- FastAPI 422 detail is an array -> map detail.map(e => e.msg).join(', ').
- shadcn @-folder quirk: after each `npx shadcn add <c>`, move files out
  of a stray `@` folder into src/, then delete `@`.
- slowapi Limiter.enabled = False set at conftest module level (uses
  .enabled, the public attr, not ._enabled).
- pyproject.toml needs [tool.pytest.ini_options] pythonpath=["."].

## To run (once built)
Backend:  cd "F:\repos\roadmap-solutions\Python\Expense Tracker API\backend"
          uv run uvicorn app.main:app --reload  ->  http://localhost:8000/docs
Frontend: cd "F:\repos\roadmap-solutions\Python\Expense Tracker API\frontend"
          npm run dev  ->  http://localhost:5173

## Verification (end-to-end)
1. Backend /docs: register -> login -> POST expense -> GET list (each
   range) -> GET summary -> PATCH -> DELETE.
2. uv run pytest — target all passing (auth, CRUD, filters, summary,
   ownership-404).
3. Frontend manual flow: register (with name) -> login -> add expense ->
   dashboard cards + list update -> switch range presets -> filter by
   category on Expenses page -> edit -> delete -> logout.
   Confirm `npm run build` (tsc) is clean.
