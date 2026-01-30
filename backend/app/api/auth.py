"""
Authentication API Routes
"""
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.user import (
    UserCreate,
    UserResponse,
    UserLogin,
    PasswordResetCreate,
    PasswordResetVerify,
    ChangePassword
)
from app.schemas.auth import Token
from app.services.auth_service import (
    create_user,
    authenticate_user,
    update_user_password,
    create_password_reset_token,
    verify_password_reset_token
)
from app.core.security import create_access_token
from app.core.deps import get_current_user
from app.config import settings

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=dict, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user

    - **email**: User email (must be unique)
    - **password**: Password (min 8 characters, must contain letter and digit)
    - **nickname**: Optional user nickname
    """
    new_user = create_user(user_data, db)

    return {
        "code": 201,
        "message": "Registration successful",
        "data": {
            "user_id": new_user.id,
            "email": new_user.email,
            "nickname": new_user.nickname
        }
    }


@router.post("/login", response_model=dict)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Login with email and password

    - **username**: Email address
    - **password**: Password

    Returns JWT token valid for 7 days
    """
    user, error_msg = authenticate_user(form_data.username, form_data.password, db)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=error_msg,
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.id, "email": user.email},
        expires_delta=access_token_expires
    )

    return {
        "code": 200,
        "data": {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": settings.access_token_expire_minutes * 60,
            "user": {
                "id": user.id,
                "email": user.email,
                "nickname": user.nickname
            }
        }
    }


@router.get("/me", response_model=dict)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Get current authenticated user information
    """
    return {
        "code": 200,
        "data": {
            "id": current_user.id,
            "email": current_user.email,
            "nickname": current_user.nickname,
            "created_at": current_user.created_at.isoformat(),
            "last_login_at": current_user.last_login_at.isoformat() if current_user.last_login_at else None
        }
    }


@router.post("/logout", response_model=dict)
async def logout(current_user: User = Depends(get_current_user)):
    """
    Logout current user

    Note: JWT tokens are stateless, so actual token invalidation
    would require a blacklist or token expiration.
    This endpoint is provided for API completeness.
    """
    return {
        "code": 200,
        "message": "Logout successful"
    }


@router.put("/change-password", response_model=dict)
async def change_password(
    password_data: ChangePassword,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Change user password

    - **old_password**: Current password
    - **new_password**: New password (min 8 characters, must contain letter and digit)
    """
    update_user_password(current_user, password_data.old_password, password_data.new_password, db)

    return {
        "code": 200,
        "message": "Password changed successfully"
    }


@router.post("/forgot-password", response_model=dict)
async def forgot_password(
    request: PasswordResetCreate,
    db: Session = Depends(get_db)
):
    """
    Request password reset email

    - **email**: User email address

    Note: In production, this would send an email with the reset token.
    For development, the token is returned in the response.
    """
    try:
        token = create_password_reset_token(request.email, db)

        # In production, send email here
        # For development, return token in response
        return {
            "code": 200,
            "message": "Password reset email sent",
            "data": {
                "token": token  # Remove this in production
            }
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process password reset request: {str(e)}"
        )


@router.post("/reset-password", response_model=dict)
async def reset_password(
    request: PasswordResetVerify,
    db: Session = Depends(get_db)
):
    """
    Reset password using token

    - **token**: Password reset token from email
    - **new_password**: New password (min 8 characters, must contain letter and digit)
    """
    try:
        verify_password_reset_token(request.token, request.new_password, db)

        return {
            "code": 200,
            "message": "Password reset successful"
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to reset password: {str(e)}"
        )
