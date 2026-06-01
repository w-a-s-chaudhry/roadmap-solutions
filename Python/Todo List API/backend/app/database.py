# Author:      Wajid Ali Chaudhry
# Description: Database engine, session factory, and Base class.
#              Every other file imports from here.

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todos.db")

# The engine is the actual connection to the database file.
# check_same_thread=False is required for SQLite when used
# with FastAPI — FastAPI handles requests across threads and
# SQLite's default safety check would block this.
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# SessionLocal is a factory — calling SessionLocal() gives
# you a new database session. Each request gets its own
# session so they don't interfere with each other.
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Base is the parent class all models inherit from.
# SQLAlchemy uses it to track which classes are tables.
class Base(DeclarativeBase):
    pass
