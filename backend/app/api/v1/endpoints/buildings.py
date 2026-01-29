"""
建筑数据管理API端点
"""
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import datetime
import logging

from app.core.database import get_db
from app.schemas.building import (
    BuildingCreate,
    BuildingUpdate,
    BuildingResponse,
    BuildingListResponse,
    BBoxQuery,
)
from app.services.building_service import BuildingService
from app.utils.logger import logger

router = APIRouter()


@router.get("/", response_model=BuildingListResponse)
async def get_buildings(
    min_lat: float = Query(..., ge=-90, le=90, description="最小纬度"),
    max_lat: float = Query(..., ge=-90, le=90, description="最大纬度"),
    min_lng: float = Query(..., ge=-180, le=180, description="最小经度"),
    max_lng: float = Query(..., ge=-180, le=180, description="最大经度"),
    include_shadow: bool = Query(False, description="是否包含阴影数据"),
    analysis_date: Optional[str] = Query(None, description="分析日期 YYYY-MM-DD"),
    analysis_hour: Optional[int] = Query(None, ge=0, le=23, description="分析小时"),
    db: AsyncSession = Depends(get_db),
):
    """
    获取视野范围内的建筑列表

    使用Bounding Box查询优化性能
    """
    try:
        logger.info(f"查询建筑范围: lat[{min_lat}, {max_lat}], lng[{min_lng}, {max_lng}]")

        service = BuildingService(db)
        buildings = await service.get_buildings_in_bbox(
            min_lat=min_lat,
            max_lat=max_lat,
            min_lng=min_lng,
            max_lng=max_lng,
            include_shadow=include_shadow,
            analysis_date=analysis_date,
            analysis_hour=analysis_hour,
        )

        return BuildingListResponse(
            code=200,
            data={
                "buildings": buildings,
                "total": len(buildings),
            },
        )

    except Exception as e:
        logger.error(f"获取建筑列表失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取建筑列表失败: {str(e)}")


@router.get("/{building_id}", response_model=BuildingResponse)
async def get_building(
    building_id: int,
    db: AsyncSession = Depends(get_db),
):
    """获取单个建筑详情"""
    try:
        service = BuildingService(db)
        building = await service.get_building_by_id(building_id)

        if not building:
            raise HTTPException(status_code=404, detail=f"建筑ID {building_id} 不存在")

        return BuildingResponse(
            code=200,
            data=building,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取建筑详情失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取建筑详情失败: {str(e)}")


@router.post("/", response_model=BuildingResponse, status_code=201)
async def create_building(
    building: BuildingCreate,
    db: AsyncSession = Depends(get_db),
):
    """创建新建筑"""
    try:
        service = BuildingService(db)
        new_building = await service.create_building(building)

        return BuildingResponse(
            code=201,
            data=new_building,
        )

    except Exception as e:
        logger.error(f"创建建筑失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"创建建筑失败: {str(e)}")


@router.put("/{building_id}", response_model=BuildingResponse)
async def update_building(
    building_id: int,
    building: BuildingUpdate,
    db: AsyncSession = Depends(get_db),
):
    """更新建筑信息"""
    try:
        service = BuildingService(db)
        updated_building = await service.update_building(building_id, building)

        if not updated_building:
            raise HTTPException(status_code=404, detail=f"建筑ID {building_id} 不存在")

        return BuildingResponse(
            code=200,
            data=updated_building,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"更新建筑失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"更新建筑失败: {str(e)}")


@router.delete("/{building_id}")
async def delete_building(
    building_id: int,
    db: AsyncSession = Depends(get_db),
):
    """删除建筑"""
    try:
        service = BuildingService(db)
        success = await service.delete_building(building_id)

        if not success:
            raise HTTPException(status_code=404, detail=f"建筑ID {building_id} 不存在")

        return {
            "code": 200,
            "message": f"建筑 {building_id} 删除成功",
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"删除建筑失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"删除建筑失败: {str(e)}")


@router.post("/import")
async def import_buildings(
    file: UploadFile = File(...),
    city: Optional[str] = Query(None, description="城市名称"),
    db: AsyncSession = Depends(get_db),
):
    """
    导入建筑数据

    支持格式: GeoJSON, Shapefile, KML
    """
    try:
        service = BuildingService(db)

        # 验证文件类型
        if not file.filename.endswith((".geojson", ".json", ".shp", ".kml")):
            raise HTTPException(
                status_code=400,
                detail="不支持的文件格式，请使用 GeoJSON, Shapefile 或 KML",
            )

        result = await service.import_buildings(file, city)

        return {
            "code": 201,
            "data": result,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"导入建筑数据失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"导入建筑数据失败: {str(e)}")
