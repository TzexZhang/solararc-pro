"""
Authentication Schemas
"""
from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    """JWT Token schema"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: Optional[dict] = None


class TokenData(BaseModel):
    """Token data schema"""
    email: Optional[str] = None
    user_id: Optional[str] = None
