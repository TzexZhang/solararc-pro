"""
Authentication Service
"""
from datetime import datetime, timedelta
from typing import Optional, Tuple
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User, PasswordReset
from app.schemas.user import UserCreate, UserInDB
from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.utils import validate_email, validate_password_strength
from app.config import settings


def create_user(user_data: UserCreate, db: Session) -> UserInDB:
    """
    Create a new user

    Args:
        user_data: User creation data
        db: Database session

    Returns:
        Created user

    Raises:
        HTTPException: If email already exists or validation fails
    """
    # Validate email
    if not validate_email(user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format"
        )

    # Validate password strength
    is_valid, error_msg = validate_password_strength(user_data.password)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_msg
        )

    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create new user
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        password_hash=hashed_password,
        nickname=user_data.nickname,
        is_active=True,
        is_locked=False,
        failed_login_count=0
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def authenticate_user(email: str, password: str, db: Session) -> Tuple[Optional[User], Optional[str]]:
    """
    Authenticate user with email and password

    Args:
        email: User email
        password: User password
        db: Database session

    Returns:
        Tuple of (user, error_message)
    """
    # Query user by email
    user = db.query(User).filter(User.email == email).first()

    if not user:
        return None, "Invalid email or password"

    # Check if user is locked
    if user.is_locked:
        # Check if lock has expired
        if user.locked_until and user.locked_until < datetime.utcnow():
            # Unlock the account
            user.is_locked = False
            user.failed_login_count = 0
            user.locked_until = None
            db.commit()
        else:
            return None, f"Account is locked due to too many failed login attempts. Try again after {user.locked_until}"

    # Verify password
    if not verify_password(password, user.password_hash):
        # Increment failed login count
        user.failed_login_count += 1

        # Lock account if too many failed attempts
        if user.failed_login_count >= 5:
            user.is_locked = True
            user.locked_until = datetime.utcnow() + timedelta(minutes=30)

        db.commit()
        return None, "Invalid email or password"

    # Reset failed login count on successful login
    if user.failed_login_count > 0:
        user.failed_login_count = 0
        user.last_login_at = datetime.utcnow()

    db.commit()

    return user, None


def update_user_password(user: User, old_password: str, new_password: str, db: Session) -> bool:
    """
    Update user password

    Args:
        user: User object
        old_password: Old password
        new_password: New password
        db: Database session

    Returns:
        True if password updated successfully

    Raises:
        HTTPException: If old password is incorrect or new password is weak
    """
    # Verify old password
    if not verify_password(old_password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect old password"
        )

    # Validate new password strength
    is_valid, error_msg = validate_password_strength(new_password)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_msg
        )

    # Update password
    user.password_hash = get_password_hash(new_password)
    db.commit()

    return True


def create_password_reset_token(email: str, db: Session) -> str:
    """
    Create password reset token

    Args:
        email: User email
        db: Database session

    Returns:
        Reset token

    Raises:
        HTTPException: If user not found
    """
    # Find user by email
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Create reset token
    from app.core.security import create_access_token
    token = create_access_token(
        data={"sub": user.id, "type": "password_reset"},
        expires_delta=timedelta(hours=1)
    )

    # Save to database
    reset_record = PasswordReset(
        user_id=user.id,
        token=token,
        expires_at=datetime.utcnow() + timedelta(hours=1),
        used=False
    )

    db.add(reset_record)
    db.commit()

    return token


def verify_password_reset_token(token: str, new_password: str, db: Session) -> bool:
    """
    Verify password reset token and update password

    Args:
        token: Reset token
        new_password: New password
        db: Database session

    Returns:
        True if password reset successful

    Raises:
        HTTPException: If token is invalid or expired
    """
    from app.core.security import decode_access_token

    # Decode token
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired token"
        )

    # Check token type
    if payload.get("type") != "password_reset":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token type"
        )

    # Get user ID
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token"
        )

    # Find reset record
    reset_record = db.query(PasswordReset).filter(
        PasswordReset.token == token,
        PasswordReset.used == False
    ).first()

    if not reset_record or reset_record.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired token"
        )

    # Get user
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Validate new password
    is_valid, error_msg = validate_password_strength(new_password)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_msg
        )

    # Update password
    user.password_hash = get_password_hash(new_password)
    user.failed_login_count = 0
    user.is_locked = False

    # Mark reset token as used
    reset_record.used = True

    db.commit()

    return True
