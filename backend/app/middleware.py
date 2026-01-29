"""
中间件模块
"""
from fastapi import Request
import time

from app.config import settings
from app.utils.logger import logger


async def request_timing_middleware(request: Request, call_next):
    """
    请求计时中间件

    记录每个请求的处理时间，并在响应头中添加处理时间
    """
    start_time = time.time()

    # 记录请求开始
    logger.info(f"Request started: {request.method} {request.url.path}")

    try:
        response = await call_next(request)
        process_time = time.time() - start_time

        # 添加处理时间到响应头
        response.headers["X-Process-Time"] = str(process_time)

        # 记录慢请求
        if settings.ENABLE_PERFORMANCE_MONITORING and process_time > settings.SLOW_QUERY_THRESHOLD:
            logger.warning(f"Slow request: {request.method} {request.url.path} took {process_time:.2f}s")
        else:
            logger.info(f"Request completed: {request.method} {request.url.path} in {process_time:.2f}s")

        return response

    except Exception as e:
        process_time = time.time() - start_time
        logger.error(f"Request failed: {request.method} {request.url.path} after {process_time:.2f}s - {str(e)}")
        raise
