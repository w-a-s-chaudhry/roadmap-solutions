# Author:      Wajid Ali Chaudhry
# Description: SQLAlchemy models — one class per database table.
#              User owns many Todos (one-to-many relationship).

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)

    # Never store the plain password — only the bcrypt hash.
    hashed_password = Column(String, nullable=False)

    is_active = Column(Boolean, default=True)

    # func.now() tells the DB to set this to the current
    # timestamp when the row is created.
    created_at = Column(DateTime, server_default=func.now())

    # back_populates links this to Todo.owner so both sides
    # of the relationship are aware of each other.
    todos = relationship("Todo", back_populates="owner")


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    done = Column(Boolean, default=False)

    # Priority 1 (low) to 5 (high)
    priority = Column(Integer, default=1)

    created_at = Column(DateTime, server_default=func.now())

    # onupdate automatically refreshes this whenever the
    # row is updated — no manual work needed.
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # ForeignKey creates the link: this todo belongs to a user.
    # nullable=False means every todo must have an owner.
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="todos")
