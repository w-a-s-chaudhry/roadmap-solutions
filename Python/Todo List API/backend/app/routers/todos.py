# Author:      Wajid Ali Chaudhry
# Description: Todo CRUD endpoints — all require auth.
#              Ownership enforced via 404 (hide existence).

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session

from app import models, schemas
from app.dependencies import get_db, get_current_user

router = APIRouter(prefix="/todos", tags=["todos"])


# --- Helpers ---


# Fetch a todo by id, 404 if missing or not owned by the user
def _get_owned_todo(db: Session, todo_id: int, user: models.User):
    todo = (
        db.query(models.Todo)
        .filter(models.Todo.id == todo_id, models.Todo.owner_id == user.id)
        .first()
    )
    if todo is None:
        raise HTTPException(404, detail="Todo not found")
    return todo


# --- Endpoints ---


# Create a new todo owned by the current user
@router.post(
    "",
    response_model=schemas.TodoResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_todo(
    body: schemas.TodoCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    new_todo = models.Todo(
        title=body.title,
        description=body.description,
        priority=body.priority,
        owner_id=current_user.id,
    )

    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo


# List the current user's todos with filter, sort, pagination
@router.get("", response_model=schemas.PaginatedTodos)
def list_todos(
    page: int = 1,
    size: int = 10,
    done: bool | None = None,
    priority: int | None = None,
    sort: str = "created_at",
    order: str = "desc",
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    q = db.query(models.Todo).filter(models.Todo.owner_id == current_user.id)

    if done is not None:
        q = q.filter(models.Todo.done == done)
    if priority is not None:
        q = q.filter(models.Todo.priority == priority)

    column = getattr(models.Todo, sort)
    q = q.order_by(desc(column) if order == "desc" else asc(column))
    total = q.count()
    offset = (page - 1) * size
    items = q.offset(offset).limit(size).all()
    pages = -(-total // size)

    return {"items": items, "total": total, "page": page, "size": size, "pages": pages}


# Get one todo by id (must be owned by current user)
@router.get("/{todo_id}", response_model=schemas.TodoResponse)
def get_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return _get_owned_todo(db, todo_id, current_user)


# Update fields on a todo; only fields sent in the body change
@router.patch("/{todo_id}", response_model=schemas.TodoResponse)
def update_todo(
    todo_id: int,
    body: schemas.TodoUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    todo = _get_owned_todo(db, todo_id, current_user)
    updates = body.model_dump(exclude_unset=True)

    for field, value in updates.items():
        setattr(todo, field, value)

    db.commit()
    db.refresh(todo)

    return todo


# Delete a todo; returns 204 No Content
@router.delete(
    "/{todo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    todo = _get_owned_todo(db, todo_id, current_user)
    db.delete(todo)
    db.commit()
    return None
