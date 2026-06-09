# Author: Wajid Ali Saleem Chaudhry
# Description: Expense CRUD endpoints — all require auth.
#              Ownership enforced via 404 (hide existence).

from datetime import date, timedelta
from decimal import Decimal
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import asc, desc, func
from sqlalchemy.orm import Session

from app import models, schemas
from app.models import CategoryEnum
from app.dependencies import get_db, get_current_user

router = APIRouter(prefix="/expenses", tags=["expenses"])

# --- Helpers ---


# Fetch an expense by id; 404 if missing or not owned by user
def _get_owned_expense(db: Session, expense_id: int, user: models.User):
    expense = (
        db.query(models.Expense)
        .filter(
            models.Expense.id == expense_id,
            models.Expense.owner_id == user.id,
        )
        .first()
    )
    if expense is None:
        raise HTTPException(404, detail="Expense not found")
    return expense


# Resolve a named range (or "custom") into (start, end) dates
def _resolve_range(
    range: Optional[str],
    start_date: Optional[date],
    end_date: Optional[date],
) -> tuple[date, date]:
    today = date.today()

    if range == "custom":
        if start_date is None or end_date is None:
            raise HTTPException(422, "start_date and end_date required")
        start, end = start_date, end_date
    elif range == "past_week":
        start, end = today - timedelta(days=7), today
    elif range == "past_month":
        start, end = today - timedelta(days=30), today
    elif range == "last_3_months":
        start, end = today - timedelta(days=90), today
    else:
        start, end = today - timedelta(days=30), today

    return start, end


# --- Endpoints ---


# Create a new expense owned by the current user
@router.post(
    "",
    response_model=schemas.ExpenseResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_expense(
    body: schemas.ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    new_expense = models.Expense(
        title=body.title,
        amount=body.amount,
        date=body.date,
        category=body.category,
        owner_id=current_user.id,
    )

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense


# List the current user's expenses with filter, sort, pagination
@router.get("", response_model=schemas.PaginatedExpenses)
def list_expenses(
    page: int = 1,
    size: int = 10,
    category: CategoryEnum | None = None,
    sort: str = "created_at",
    order: str = "desc",
    range: Optional[str] = Query(default="past_month"),
    start_date: Optional[date] = Query(default=None),
    end_date: Optional[date] = Query(default=None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    start, end = _resolve_range(range, start_date, end_date)

    q = db.query(models.Expense).filter(models.Expense.owner_id == current_user.id)

    q = q.filter(
        models.Expense.date >= start,
        models.Expense.date <= end,
    )

    if category is not None:
        q = q.filter(models.Expense.category == category)

    column = getattr(models.Expense, sort)
    q = q.order_by(desc(column) if order == "desc" else asc(column))
    total = q.count()
    offset = (page - 1) * size
    items = q.offset(offset).limit(size).all()
    pages = -(-total // size)

    return {
        "items": items,
        "total": total,
        "page": page,
        "size": size,
        "pages": pages,
    }


# Return spend summary for the dashboard cards
# NOTE: must be declared before /{expense_id} — FastAPI matches
#       routes top-to-bottom, so "summary" would be read as an id
@router.get("/summary", response_model=schemas.ExpenseSummary)
def get_summary(
    range: Optional[str] = Query(default="past_month"),
    start_date: Optional[date] = Query(default=None),
    end_date: Optional[date] = Query(default=None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    start, end = _resolve_range(range, start_date, end_date)

    total_spent, count = (
        db.query(func.sum(models.Expense.amount), func.count(models.Expense.id))
        .filter(
            models.Expense.owner_id == current_user.id,
            models.Expense.date >= start,
            models.Expense.date <= end,
        )
        .one()
    )
    total_spent = total_spent or Decimal("0.00")

    row = (
        db.query(models.Expense.category)
        .filter(
            models.Expense.owner_id == current_user.id,
            models.Expense.date >= start,
            models.Expense.date <= end,
        )
        .group_by(models.Expense.category)
        .order_by(func.sum(models.Expense.amount).desc())
        .first()
    )
    top_category = row[0].value if row else None

    return schemas.ExpenseSummary(
        total_spent=total_spent,
        count=count,
        top_category=top_category,
    )


# Get one expense by id (must be owned by current user)
@router.get("/{expense_id}", response_model=schemas.ExpenseResponse)
def get_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return _get_owned_expense(db, expense_id, current_user)


# Update fields on an expense; only fields sent in the body change
@router.patch("/{expense_id}", response_model=schemas.ExpenseResponse)
def update_expense(
    expense_id: int,
    body: schemas.ExpenseUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    expense = _get_owned_expense(db, expense_id, current_user)
    updates = body.model_dump(exclude_unset=True)

    for field, value in updates.items():
        setattr(expense, field, value)

    db.commit()
    db.refresh(expense)

    return expense


# Delete an expense; returns 204 No Content
@router.delete(
    "/{expense_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    expense = _get_owned_expense(db, expense_id, current_user)
    db.delete(expense)
    db.commit()
    return None
