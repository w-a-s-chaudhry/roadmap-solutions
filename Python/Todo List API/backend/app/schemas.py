# Author:       Wajid Ali Saleem Chaudhry
# Description:  Pydantic Schemas: shapes of API request/response data

from pydantic import BaseModel, EmailStr
from datetime import datetime

# --- User schemas ---


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# --- Auth schemas ---
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: str


# --- Todo schemas ---


class TodoCreate(BaseModel):
    title: str
    description: str | None = None
    priority: int = 1


class TodoUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    done: bool | None = None
    priority: int | None = None


class TodoResponse(BaseModel):
    id: int
    title: str
    description: str | None
    done: bool
    priority: int
    created_at: datetime
    updated_at: datetime
    owner_id: int

    class Config:
        from_attributes = True


class PaginatedTodos(BaseModel):
    items: list[TodoResponse]
    total: int
    page: int
    size: int
    pages: int
