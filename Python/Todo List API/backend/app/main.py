# Author:      Wajid Ali Chaudhry
# Description: FastAPI application entry point. Creates the app,
#              registers routers, and creates DB tables on startup.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routers import users, todos

from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.limiter import limiter


# Import models so SQLAlchemy knows they exist before
# create_all() is called — without this the tables won't appear.
import app.models  # noqa: F401

app = FastAPI(
    title="Todo List API",
    description="A REST API for managing todos with JWT auth.",
    version="1.0.0",
)


app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS lets the frontend (running on a different port) call
# this API. In development we allow all origins; tighten
# this in production to your actual frontend domain.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Register Router ---
app.include_router(users.router)
app.include_router(todos.router)

# --- Startup ---


@app.on_event("startup")
def create_tables():
    # Creates any tables that don't exist yet.
    # Safe to call every startup — won't drop existing data.
    Base.metadata.create_all(bind=engine)


# --- Health check ---


@app.get("/", tags=["health"])
def root():
    return {"status": "ok", "message": "Todo API is running"}
