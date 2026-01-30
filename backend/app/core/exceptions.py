"""
Custom exception classes
"""
from typing import Optional, Any


class BaseAPIException(Exception):
    """Base API exception"""

    def __init__(
        self,
        message: str,
        code: int = 400,
        error_type: str = "API_ERROR",
        details: Optional[Any] = None
    ):
        self.message = message
        self.code = code
        self.error_type = error_type
        self.details = details
        super().__init__(self.message)


class ValidationError(BaseAPIException):
    """Validation error exception"""

    def __init__(self, message: str, details: Optional[Any] = None):
        super().__init__(
            message=message,
            code=400,
            error_type="VALIDATION_ERROR",
            details=details
        )


class AuthenticationError(BaseAPIException):
    """Authentication error exception"""

    def __init__(self, message: str = "Authentication failed"):
        super().__init__(
            message=message,
            code=401,
            error_type="AUTHENTICATION_ERROR"
        )


class AuthorizationError(BaseAPIException):
    """Authorization error exception"""

    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(
            message=message,
            code=403,
            error_type="AUTHORIZATION_ERROR"
        )


class NotFoundError(BaseAPIException):
    """Resource not found error exception"""

    def __init__(self, resource: str = "Resource"):
        super().__init__(
            message=f"{resource} not found",
            code=404,
            error_type="NOT_FOUND"
        )


class ConflictError(BaseAPIException):
    """Resource conflict error exception"""

    def __init__(self, message: str):
        super().__init__(
            message=message,
            code=409,
            error_type="CONFLICT_ERROR"
        )


class DatabaseError(BaseAPIException):
    """Database error exception"""

    def __init__(self, message: str = "Database operation failed"):
        super().__init__(
            message=message,
            code=500,
            error_type="DATABASE_ERROR"
        )


class ExternalServiceError(BaseAPIException):
    """External service error exception"""

    def __init__(self, service: str, message: str = "External service error"):
        super().__init__(
            message=f"{service}: {message}",
            code=502,
            error_type="EXTERNAL_SERVICE_ERROR"
        )
