"""
日照分析API端点
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from datetime import datetime
from pydantic import BaseModel

from app.services.analysis_service import AnalysisService
from app.utils.logger import logger

router = APIRouter()


class PointSunlightRequest(BaseModel):
    """指定点日照分析请求"""
    point: dict  # {"lat": 22.5431, "lng": 114.0579}
    date: str  # YYYY-MM-DD
    start_hour: int = 6
    end_hour: int = 18


class ShadowOverlapRequest(BaseModel):
    """阴影重叠分析请求"""
    target_building_id: int
    surrounding_building_ids: list[int]
    date: str  # YYYY-MM-DD
    hour: int


@router.post("/point-sunlight")
async def analyze_point_sunlight(request: PointSunlightRequest):
    """
    分析指定点的有效日照时长

    计算该点在指定时间段内被建筑遮挡的情况
    """
    try:
        lat = request.point.get("lat")
        lng = request.point.get("lng")

        if not lat or not lng:
            raise HTTPException(status_code=400, detail="必须提供经纬度坐标")

        logger.info(
            f"分析点日照: lat={lat}, lng={lng}, "
            f"date={request.date}, time={request.start_hour}:00-{request.end_hour}:00"
        )

        service = AnalysisService()

        # 解析日期
        try:
            target_date = datetime.strptime(request.date, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(status_code=400, detail="日期格式错误，请使用 YYYY-MM-DD")

        # 分析日照
        result = await service.analyze_point_sunlight(
            latitude=lat,
            longitude=lng,
            target_date=target_date,
            start_hour=request.start_hour,
            end_hour=request.end_hour,
        )

        return {
            "code": 200,
            "data": result,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"分析点日照失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"分析点日照失败: {str(e)}")


@router.post("/shadow-overlap")
async def analyze_shadow_overlap(request: ShadowOverlapRequest):
    """
    阴影重叠分析

    分析目标建筑与周围建筑的阴影重叠情况
    """
    try:
        logger.info(
            f"分析阴影重叠: target={request.target_building_id}, "
            f"surrounding={len(request.surrounding_building_ids)}, "
            f"date={request.date}, hour={request.hour}"
        )

        service = AnalysisService()

        # 解析日期
        try:
            target_date = datetime.strptime(request.date, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(status_code=400, detail="日期格式错误，请使用 YYYY-MM-DD")

        # 分析阴影重叠
        result = await service.analyze_shadow_overlap(
            target_building_id=request.target_building_id,
            surrounding_building_ids=request.surrounding_building_ids,
            target_date=target_date,
            hour=request.hour,
        )

        return {
            "code": 200,
            "data": result,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"分析阴影重叠失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"分析阴影重叠失败: {str(e)}")


@router.get("/building-sunlight/{building_id}")
async def analyze_building_sunlight(
    building_id: int,
    date: str = Query(..., description="日期 YYYY-MM-DD"),
):
    """
    分析建筑的整体日照情况

    计算建筑各个立面的日照时长
    """
    try:
        logger.info(f"分析建筑日照: building={building_id}, date={date}")

        service = AnalysisService()

        # 解析日期
        try:
            target_date = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(status_code=400, detail="日期格式错误，请使用 YYYY-MM-DD")

        # 分析建筑日照
        result = await service.analyze_building_sunlight(
            building_id=building_id,
            target_date=target_date,
        )

        return {
            "code": 200,
            "data": result,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"分析建筑日照失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"分析建筑日照失败: {str(e)}")


@router.get("/annual-sunlight/{building_id}")
async def analyze_annual_sunlight(
    building_id: int,
    year: Optional[int] = Query(None, description="年份，默认当年"),
):
    """
    分析建筑的年度日照情况

    计算全年四季的平均日照时长
    """
    try:
        if year is None:
            year = datetime.now().year

        logger.info(f"分析年度日照: building={building_id}, year={year}")

        service = AnalysisService()

        # 分析年度日照
        result = await service.analyze_annual_sunlight(
            building_id=building_id,
            year=year,
        )

        return {
            "code": 200,
            "data": result,
        }

    except Exception as e:
        logger.error(f"分析年度日照失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"分析年度日照失败: {str(e)}")


@router.get("/standard-compliance/{building_id}")
async def check_standard_compliance(
    building_id: int,
    standard: str = Query("GB50180-2018", description="日照标准（默认GB50180-2018）"),
):
    """
    检查建筑是否符合日照标准

    根据国家或地方标准判断建筑日照是否合规
    """
    try:
        logger.info(f"检查日照标准合规: building={building_id}, standard={standard}")

        service = AnalysisService()

        # 检查合规性
        result = await service.check_standard_compliance(
            building_id=building_id,
            standard=standard,
        )

        return {
            "code": 200,
            "data": result,
        }

    except Exception as e:
        logger.error(f"检查日照标准合规失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"检查日照标准合规失败: {str(e)}")
