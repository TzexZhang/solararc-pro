"""
坐标系转换API端点

支持 WGS84, GCJ-02, BD-09 三种坐标系之间的相互转换
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel

from app.services.coord_system_service import CoordSystemService
from app.utils.logger import logger

router = APIRouter()


class CoordTransformRequest(BaseModel):
    """坐标转换请求"""
    coords: List[dict]  # [{"lng": 116.397428, "lat": 39.90923}, ...]
    from_system: str  # WGS84, GCJ02, BD09
    to_system: str  # WGS84, GCJ02, BD09


class BatchCoordTransformRequest(BaseModel):
    """批量坐标转换请求（GeoJSON格式）"""
    geojson: dict
    from_system: str
    to_system: str


@router.post("/transform")
async def transform_coordinates(request: CoordTransformRequest):
    """
    转换坐标到目标坐标系

    支持 WGS84, GCJ-02, BD-09 之间的相互转换
    """
    try:
        # 验证坐标系
        valid_systems = ["WGS84", "GCJ02", "BD09"]
        if request.from_system not in valid_systems:
            raise HTTPException(
                status_code=400,
                detail=f"源坐标系无效，必须是: {', '.join(valid_systems)}"
            )
        if request.to_system not in valid_systems:
            raise HTTPException(
                status_code=400,
                detail=f"目标坐标系无效，必须是: {', '.join(valid_systems)}"
            )

        logger.info(
            f"坐标转换: {request.from_system} -> {request.to_system}, "
            f"点数={len(request.coords)}"
        )

        service = CoordSystemService()

        # 转换坐标
        transformed = await service.transform_coordinates(
            coordinates=request.coords,
            from_system=request.from_system,
            to_system=request.to_system,
        )

        return {
            "code": 200,
            "data": {
                "coordinates": transformed,
                "from_system": request.from_system,
                "to_system": request.to_system,
                "count": len(transformed),
            },
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"坐标转换失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"坐标转换失败: {str(e)}")


@router.post("/transform-geojson")
async def transform_geojson(request: BatchCoordTransformRequest):
    """
    转换GeoJSON中的坐标

    批量转换GeoJSON中的所有坐标点
    """
    try:
        # 验证坐标系
        valid_systems = ["WGS84", "GCJ02", "BD09"]
        if request.from_system not in valid_systems:
            raise HTTPException(
                status_code=400,
                detail=f"源坐标系无效，必须是: {', '.join(valid_systems)}"
            )
        if request.to_system not in valid_systems:
            raise HTTPException(
                status_code=400,
                detail=f"目标坐标系无效，必须是: {', '.join(valid_systems)}"
            )

        logger.info(
            f"GeoJSON坐标转换: {request.from_system} -> {request.to_system}"
        )

        service = CoordSystemService()

        # 转换GeoJSON
        transformed_geojson = await service.transform_geojson(
            geojson=request.geojson,
            from_system=request.from_system,
            to_system=request.to_system,
        )

        return {
            "code": 200,
            "data": {
                "geojson": transformed_geojson,
                "from_system": request.from_system,
                "to_system": request.to_system,
            },
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"GeoJSON坐标转换失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"GeoJSON坐标转换失败: {str(e)}")


@router.get("/offset/{lat}/{lng}")
async def get_coord_offset(
    lat: float = Query(..., ge=-90, le=90),
    lng: float = Query(..., ge=-180, le=180),
    system: str = Query("GCJ02", description="目标坐标系"),
):
    """
    获取WGS84坐标到指定坐标系的偏移量

    返回坐标在指定坐标系中的偏移距离
    """
    try:
        service = CoordSystemService()

        offset = await service.get_coord_offset(
            latitude=lat,
            longitude=lng,
            target_system=system,
        )

        return {
            "code": 200,
            "data": {
                "original": {"lat": lat, "lng": lng},
                "offset": offset,
                "target_system": system,
            },
        }

    except Exception as e:
        logger.error(f"获取坐标偏移失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取坐标偏移失败: {str(e)}")


@router.get("/detect/{lat}/{lng}")
async def detect_coord_system(
    lat: float = Query(..., ge=-90, le=90),
    lng: float = Query(..., ge=-180, le=180),
    reference_city: str = Query("北京", description="参考城市"),
):
    """
    自动检测坐标所属的坐标系

    通过与城市标准坐标对比来判断坐标系类型
    """
    try:
        service = CoordSystemService()

        detected = await service.detect_coord_system(
            latitude=lat,
            longitude=lng,
            reference_city=reference_city,
        )

        return {
            "code": 200,
            "data": detected,
        }

    except Exception as e:
        logger.error(f"检测坐标系失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"检测坐标系失败: {str(e)}")


@router.get("/systems")
async def list_coord_systems():
    """
    列出支持的坐标系

    返回系统支持的所有坐标系及其说明
    """
    return {
        "code": 200,
        "data": {
            "systems": [
                {
                    "code": "WGS84",
                    "name": "World Geodetic System 1984",
                    "description": "全球标准坐标系，GPS原始坐标",
                    "used_by": ["GPS", "国际地图"],
                },
                {
                    "code": "GCJ02",
                    "name": "国测局坐标系",
                    "description": "中国加密坐标系，也称火星坐标系",
                    "used_by": ["高德地图", "腾讯地图", "天地图"],
                },
                {
                    "code": "BD09",
                    "name": "百度坐标系",
                    "description": "百度在GCJ02基础上二次加密的坐标系",
                    "used_by": ["百度地图"],
                },
            ],
            "default": "GCJ02",
            "auto_transform": True,
        },
    }
