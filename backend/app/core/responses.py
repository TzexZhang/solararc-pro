"""
Standard API response formats
"""
from typing import Any, Optional, List, Dict
from fastapi import status
from fastapi.responses import JSONResponse


class APIResponse:
    """Standard API response builder"""

    @staticmethod
    def success(
        data: Any = None,
        message: Optional[str] = None,
        code: int = 200,
        metadata: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Build success response

        Args:
            data: Response data
            message: Optional message
            code: HTTP status code
            metadata: Optional metadata

        Returns:
            Formatted response dictionary
        """
        response = {
            "code": code,
            "message": message or "Success"
        }

        if data is not None:
            response["data"] = data

        if metadata:
            response["metadata"] = metadata

        return response

    @staticmethod
    def error(
        error: str,
        code: int = 400,
        details: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Build error response

        Args:
            error: Error message
            code: HTTP status code
            details: Optional error details

        Returns:
            Formatted error response dictionary
        """
        response = {
            "code": code,
            "error": error
        }

        if details is not None:
            response["details"] = details

        return response

    @staticmethod
    def paginated(
        data: List[Any],
        total: int,
        page: int = 1,
        page_size: int = 20,
        message: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Build paginated response

        Args:
            data: List of items
            total: Total number of items
            page: Current page number
            page_size: Items per page
            message: Optional message

        Returns:
            Formatted paginated response
        """
        total_pages = (total + page_size - 1) // page_size if page_size > 0 else 0

        return APIResponse.success(
            data={
                "items": data,
                "pagination": {
                    "total": total,
                    "page": page,
                    "page_size": page_size,
                    "total_pages": total_pages,
                    "has_next": page < total_pages,
                    "has_prev": page > 1
                }
            },
            message=message
        )


def success_response(
    data: Any = None,
    message: Optional[str] = None,
    code: int = status.HTTP_200_OK
) -> JSONResponse:
    """
    Create success JSON response

    Args:
        data: Response data
        message: Optional message
        code: HTTP status code

    Returns:
        JSONResponse
    """
    return JSONResponse(
        status_code=code,
        content=APIResponse.success(data=data, message=message, code=code)
    )


def error_response(
    error: str,
    code: int = status.HTTP_400_BAD_REQUEST,
    details: Optional[Any] = None
) -> JSONResponse:
    """
    Create error JSON response

    Args:
        error: Error message
        code: HTTP status code
        details: Optional error details

    Returns:
        JSONResponse
    """
    return JSONResponse(
        status_code=code,
        content=APIResponse.error(error=error, code=code, details=details)
    )
