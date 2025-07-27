# app/services/auth_service.py

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.utils.security import verify_password
from app.utils.jwt import create_access_token, create_refresh_token, decode_token
from app.schemas.auth import Token, TokenPayload
from app.models.user import User
from app.services.user_service import get_user_by_email
from jose import JWTError

def authenticate_user(email: str, password: str, db: Session) -> Token:
    user = get_user_by_email(email, db)
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(data={"sub": user.email})

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )

def get_current_user(token: str, db: Session) -> User:
    try:
        payload = decode_token(token)
        token_data = TokenPayload(**payload)
    except (JWTError, ValueError):
        raise HTTPException(status_code=401, detail="Invalid token")

    user = get_user_by_email(token_data.sub, db)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user

def refresh_access_token(refresh_token: str, db: Session) -> str:
    try:
        payload = decode_token(refresh_token)
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        user = get_user_by_email(email, db)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        new_access_token = create_access_token(data={"sub": user.email})
        return new_access_token

    except Exception:
        raise HTTPException(status_code=401, detail="Could not refresh token")
