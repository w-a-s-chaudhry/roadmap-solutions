# Author:      Wajid Ali Chaudhry
# Description: Password hashing and JWT token utilities.

import os
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
from jose import jwt
from passlib.context import CryptContext

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))

if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is not set in .env")

# CryptContext manages the hashing algorithm.
# "bcrypt" is the industry standard for passwords.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# --- Password helpers ---


# Hash a plain password — call this on registration
def hash_password(plain: str) -> str:
    return pwd_context.hash(plain)


# Verify a plain password against a stored hash
# — call this on login. Returns True or False.
def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


# --- Token helpers ---


# Create a short-lived access token
def create_access_token(data: dict) -> str:
    data_c = data.copy()
    expiry = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data_c["exp"] = expiry
    data_c["type"] = "access"
    return jwt.encode(data_c, SECRET_KEY, algorithm=ALGORITHM)


# Create a long-lived refresh token
def create_refresh_token(data: dict) -> str:
    data_c = data.copy()
    refresh = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    data_c["exp"] = refresh
    data_c["type"] = "refresh"
    return jwt.encode(data_c, SECRET_KEY, algorithm=ALGORITHM)
