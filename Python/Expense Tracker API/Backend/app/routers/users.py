# Author:      Wajid Ali Chaudhry
# Description: Auth endpoints — register, login and refresh.

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from app import models, schemas
from app.auth import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
)

from jose import jwt, JWTError
from app.dependencies import SECRET_KEY, ALGORITHM

from app.limiter import limiter

from app.dependencies import get_db, get_current_user

# prefix → all routes in this file start with /auth
# tags   → groups them in the Swagger docs
router = APIRouter(prefix="/auth", tags=["auth"])


# Create a new user account
@router.post(
    "/register",
    response_model=schemas.UserResponse,
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit("10/minute")
def register(
    request: Request,
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
):
    existing = db.query(models.User).filter(models.User.email == user.email).first()

    if existing is not None:
        raise HTTPException(409, detail="Registration Failed")

    new_user = models.User(
        name=user.name, email=user.email, hashed_password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# Log in with email + password, returns tokens
@router.post("/login", response_model=schemas.TokenResponse)
@limiter.limit("5/minute")
def login(
    request: Request,
    credentials: schemas.LoginRequest,
    db: Session = Depends(get_db),
):
    user = db.query(models.User).filter(models.User.email == credentials.email).first()
    if user is None or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(401, detail="Invalid email or password")
    payload = {"sub": str(user.id)}
    access_token = create_access_token(payload)
    refresh_token = create_refresh_token(payload)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


# Exchange a valid refresh token for a new access + refresh token pair
@router.post("/refresh", response_model=schemas.TokenResponse)
@limiter.limit("10/minute")
def refresh(
    request: Request,
    body: schemas.RefreshRequest,
    db: Session = Depends(get_db),
):
    try:
        payload = jwt.decode(body.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(401, detail="Invalid or expired refresh token")

    if payload.get("type") != "refresh":
        raise HTTPException(401, detail="Invalid or expired token")

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(401, detail="Invalid token")

    user_id = int(user_id)

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(401, detail="Invalid or expired token")

    payload_dict = {"sub": str(user_id)}
    access_token = create_access_token(payload_dict)
    refresh_token = create_refresh_token(payload_dict)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.get("/me", response_model=schemas.UserResponse)
def get_me(current_user: models.User = Depends(get_current_user)):
    return current_user
