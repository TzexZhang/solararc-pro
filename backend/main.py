"""
SolarArc Pro - 后端应用入口点

这是uvicorn启动时的入口文件
"""
from app.app import app

__all__ = ["app"]


if __name__ == "__main__":
    import uvicorn
    from app.config import settings

    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
        access_log=settings.ENABLE_REQUEST_LOGGING,
    )
