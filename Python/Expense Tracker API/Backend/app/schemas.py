# Author:       Wajid Ali Saleem Chaudhry
# Description:  Pydantic Schemas: shapes of API request/response data

from decimal import Decimal
from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime, date as Date

from app.models import CategoryEnum


# --- User Schemas ---
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    is_active: bool
    created_at: datetime


# --- Auth Schemas ---
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: str


# --- Expense Schemas ---
class ExpenseCreate(BaseModel):
    title: str
    amount: float
    date: Date
    category: CategoryEnum


class ExpenseUpdate(BaseModel):
    title: str | None = None
    amount: float | None = None
    date: Date | None = None
    category: CategoryEnum | None = None


class ExpenseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    amount: float
    date: Date
    category: CategoryEnum
    created_at: datetime
    owner_id: int


class PaginatedExpenses(BaseModel):
    items: list[ExpenseResponse]
    total: int
    page: int
    size: int
    pages: int


# Summary response for the three dashboard cards
class ExpenseSummary(BaseModel):
    total_spent: Decimal
    count: int
    top_category: str | None
