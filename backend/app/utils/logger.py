"""
日志工具配置
"""
import sys
import logging
from pathlib import Path
from loguru import logger as loguru_logger

from app.config import settings


class Logger:
    """日志工具类"""

    def __init__(self):
        """初始化日志工具"""
        self._setup_logger()

    def _setup_logger(self):
        """配置loguru日志"""
        # 移除默认handler
        loguru_logger.remove()

        # 控制台输出格式
        log_format = (
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        )

        # 添加控制台handler
        if settings.LOG_TO_CONSOLE:
            loguru_logger.add(
                sys.stdout,
                format=log_format,
                level=settings.LOG_LEVEL,
                colorize=True,
            )

        # 添加文件handler
        log_dir = Path(settings.LOG_FILE).parent
        log_dir.mkdir(parents=True, exist_ok=True)

        loguru_logger.add(
            settings.LOG_FILE,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
            level=settings.LOG_LEVEL,
            rotation=f"{settings.LOG_FILE_MAX_SIZE} MB",
            retention=f"{settings.LOG_FILE_BACKUP_COUNT} days",
            compression="zip",
            encoding="utf-8",
            enqueue=True,  # 异步写入
        )

        # 添加错误日志文件
        loguru_logger.add(
            settings.LOG_FILE.replace(".log", "_error.log"),
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
            level="ERROR",
            rotation=f"{settings.LOG_FILE_MAX_SIZE} MB",
            retention=f"{settings.LOG_FILE_BACKUP_COUNT} days",
            compression="zip",
            encoding="utf-8",
            enqueue=True,
        )


# 创建全局日志实例
_logger = Logger()
logger = loguru_logger


# 兼容标准logging模块
class InterceptHandler(logging.Handler):
    """拦截标准logging日志并转发到loguru"""

    def emit(self, record):
        """转发日志记录"""
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


# 配置标准logging使用loguru
logging.basicConfig(handlers=[InterceptHandler()], level=0)
