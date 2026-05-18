from typing import Optional
from pydantic import BaseModel, EmailStr
from app.models.auth import UserRole

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: UserRole

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None

class UserInDBBase(BaseModel):
    id: str
    username: str
    email: EmailStr
    role: UserRole
    is_active: bool

    class Config:
        from_attributes = True

class UserResponse(UserInDBBase):
    pass
