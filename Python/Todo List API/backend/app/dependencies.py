# Author:      Wajid Ali Chaudhry
# Description: Reusable FastAPI dependencies — database session
#              and current-user extraction.

import os
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app import models

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is not set in .env")

# Extracts the Bearer token from the Authorization header.
bearer_scheme = HTTPBearer()


# Yields a DB session for one request then closes it
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Verifies the JWT and returns the current User object
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(401, detail="Invalid Token")
        user_id = int(user_id)
    except (JWTError, ValueError, TypeError):
        raise HTTPException(401, detail="Invalid or expired token")

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(401, detail="User not found")
    return user
