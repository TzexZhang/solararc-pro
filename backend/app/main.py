"""
SolarArc Pro - FastAPI主应用
"""
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import time
from contextlib import asynccontextmanager

from app.config import settings
from app.api.v1 import api_router
from app.core.database import init_db
from app.utils.logger import logger


# 请求计时中间件
async def request_timing_middleware(request: Request, call_next):
    """记录请求处理时间"""
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


# 应用生命周期管理
@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用启动和关闭时的生命周期管理"""
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


# 创建FastAPI应用实例
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
    ## SolarArc Pro API

    高性能城市时空日照分析与视觉仿真平台

    ### 主要功能
    * 🏗️ 建筑数据管理
    * ☀️ 太阳位置计算
    * 🌑 阴影计算
    * 📊 日照分析
    * 📐 坐标系转换

    ### 技术栈
    * FastAPI (Python 3.10+)
    * MySQL 8.0 + 空间索引
    * pvlib (太阳位置算法)
    * Shapely (空间计算)
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)


# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 添加请求计时中间件
app.middleware("http")(request_timing_middleware)


# 注册路由
app.include_router(api_router, prefix="/api/v1")


# ==================== 全局异常处理 ====================

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """HTTP异常处理"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.status_code,
            "error": "HTTP_ERROR",
            "message": exc.detail,
            "path": str(request.url.path),
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """请求验证异常处理"""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "code": 422,
            "error": "VALIDATION_ERROR",
            "message": "请求参数验证失败",
            "details": exc.errors(),
            "path": str(request.url.path),
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """通用异常处理"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": 500,
            "error": "INTERNAL_SERVER_ERROR",
            "message": "服务器内部错误" if not settings.DEBUG else str(exc),
            "path": str(request.url.path),
        },
    )


# ==================== 健康检查端点 ====================

@app.get("/", tags=["Root"])
async def root():
    """根路径"""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "environment": settings.APP_ENV,
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """健康检查端点"""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "timestamp": time.time(),
    }


@app.get("/api/v1/health", tags=["Health"])
async def api_health_check():
    """API健康检查端点（用于Docker健康检查）"""
    return {"status": "ok"}


# ==================== 启动说明 ====================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
        access_log=settings.ENABLE_REQUEST_LOGGING,
    )
