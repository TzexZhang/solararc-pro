"""
API v1 端点模块
"""
from fastapi import APIRouter

from app.api.v1.endpoints import (
    health,
)

__all__ = ["health"]
