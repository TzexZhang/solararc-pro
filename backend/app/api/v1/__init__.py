"""
API v1 路由模块
"""
from fastapi import APIRouter

from app.api.v1.endpoints import (
    buildings,
    solar,
    shadows,
    analysis,
    health,
    coord_system,
)


api_router = APIRouter()

# 健康检查
api_router.include_router(health.router, tags=["Health"])

# 建筑数据
api_router.include_router(buildings.router, prefix="/buildings", tags=["Buildings"])

# 太阳位置计算
api_router.include_router(solar.router, prefix="/solar", tags=["Solar"])

# 阴影计算
api_router.include_router(shadows.router, prefix="/shadows", tags=["Shadows"])

# 日照分析
api_router.include_router(analysis.router, prefix="/analysis", tags=["Analysis"])

# 坐标系转换
api_router.include_router(coord_system.router, prefix="/coords", tags=["Coordinate System"])
