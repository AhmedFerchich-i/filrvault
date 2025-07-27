# app/api/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.auth import Token, LoginRequest
from app.services.auth_service import authenticate_user, refresh_access_token, get_current_user
from app.core.db import get_db
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # OAuth2PasswordRequestForm expects form fields: username and password,
    # but we're using email as username here
    token = authenticate_user(form_data.username, form_data.password, db)
    return token

@router.post("/refresh", response_model=Token)
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    new_access_token = refresh_access_token(refresh_token, db)
    return {"access_token": new_access_token, "token_type": "bearer"}

@router.get("/me")
def read_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = get_current_user(token, db)
    return user
