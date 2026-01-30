"""
Core functionality
"""
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    decode_access_token
)
from app.core.deps import get_current_user, get_db
from app.core.utils import (
    validate_email,
    validate_password_strength,
    calculate_shadow_coefficient
)

__all__ = [
    "get_password_hash",
    "verify_password",
    "create_access_token",
    "decode_access_token",
    "get_current_user",
    "get_db",
    "validate_email",
    "validate_password_strength",
    "calculate_shadow_coefficient",
]
