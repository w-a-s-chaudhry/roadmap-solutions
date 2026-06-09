# Author: Wajid Ali Saleem Chaudhry
# Description: SQLAlchemy models — one class per database table.
#              User owns many Expenses (one-to-many relationship).

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    ForeignKey,
    Integer,
    String,
    Numeric,
    DateTime,
    Enum,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base

import enum


class CategoryEnum(str, enum.Enum):
    food = "food"
    transport = "transport"
    entertainment = "entertainment"
    housing = "housing"
    healthcare = "healthcare"
    other = "other"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)

    # Never store the plain password — only the bcrypt hash.
    hashed_password = Column(String, nullable=False)

    is_active = Column(Boolean, default=True)

    # func.now() tells the DB to set this to the current
    # timestamp when the row is created.
    created_at = Column(DateTime, server_default=func.now())

    # back_populates links this to Expense.owner so both sides
    # of the relationship are aware of each other.
    expenses = relationship("Expense", back_populates="owner")


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    date = Column(Date, nullable=False)
    category = Column(Enum(CategoryEnum), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="expenses")
