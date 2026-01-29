"""
健康检查端点
"""
from fastapi import APIRouter
import time

router = APIRouter()


@router.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
    }


@router.get("/ping")
async def ping():
    """Ping检查"""
    return {"pong": True}
