"""
User Schemas
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    nickname: Optional[str] = Field(None, max_length=50)


class UserCreate(UserBase):
    """User creation schema"""
    password: str = Field(..., min_length=8, max_length=100)


class UserUpdate(BaseModel):
    """User update schema"""
    nickname: Optional[str] = Field(None, max_length=50)
    email: Optional[EmailStr] = None


class UserInDB(UserBase):
    """User in database schema"""
    id: str
    is_active: bool
    is_locked: bool
    last_login_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    """User response schema"""
    id: str
    email: str
    nickname: Optional[str] = None
    is_active: bool
    created_at: datetime
    last_login_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """User login schema"""
    email: EmailStr
    password: str


class PasswordResetCreate(BaseModel):
    """Password reset request schema"""
    email: EmailStr


class PasswordResetVerify(BaseModel):
    """Password reset verification schema"""
    token: str
    new_password: str = Field(..., min_length=8, max_length=100)


class ChangePassword(BaseModel):
    """Change password schema"""
    old_password: str
    new_password: str = Field(..., min_length=8, max_length=100)
