"""
SolarArc Pro - FastAPI应用配置
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.api.v1 import api_router
from app.middleware import request_timing_middleware
from app.lifespan import lifespan
from app.exceptions import (
    http_exception_handler,
    validation_exception_handler,
    general_exception_handler
)
from app.utils.logger import logger
import time


# ==================== FastAPI应用创建 ====================

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


# ==================== 中间件配置 ====================

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


# ==================== 路由注册 ====================

app.include_router(api_router, prefix="/api/v1")


# ==================== 全局异常处理 ====================

app.add_exception_handler(http_exception_handler)
app.add_exception_handler(validation_exception_handler)
app.add_exception_handler(general_exception_handler)


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
