from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    username: str | None = None

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str | None

    class Config:
        orm_mode = True
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None