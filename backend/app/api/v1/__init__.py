"""
API v1 路由模块
"""
from fastapi import APIRouter

# 暂时只启用健康检查端点
from app.api.v1.endpoints import health


api_router = APIRouter()

# 健康检查
api_router.include_router(health.router, tags=["Health"])

# TODO: 其他端点正在开发中
# api_router.include_router(buildings.router, prefix="/buildings", tags=["Buildings"])
# api_router.include_router(solar.router, prefix="/solar", tags=["Solar"])
# api_router.include_router(shadows.router, prefix="/shadows", tags=["Shadows"])
# api_router.include_router(analysis.router, prefix="/analysis", tags=["Analysis"])
# api_router.include_router(coord_system.router, prefix="/coords", tags=["Coordinate System"])
