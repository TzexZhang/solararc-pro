"""
应用生命周期管理模块
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.config import settings
from app.core.database import init_db
from app.utils.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    应用启动和关闭时的生命周期管理

    在应用启动时初始化数据库连接
    在应用关闭时清理资源
    """
    # 启动时执行
    logger.info("=" * 60)
    logger.info(f"🚀 {settings.APP_NAME} v{settings.APP_VERSION} 启动中...")
    logger.info(f"📍 环境: {settings.APP_ENV}")
    logger.info(f"🔗 调试模式: {settings.DEBUG}")
    logger.info(f"⏰ 时区: {settings.TZ}")
    logger.info("=" * 60)

    # 初始化数据库
    try:
        await init_db()
        logger.info("✅ 数据库初始化成功")
    except Exception as e:
        logger.error(f"❌ 数据库初始化失败: {str(e)}")
        raise

    yield

    # 关闭时执行
    logger.info("👋 应用关闭中...")
    logger.info("✅ 所有连接已关闭")
