"""
太阳位置计算API端点
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from datetime import datetime, date
import pytz

from app.services.solar_service import SolarService
from app.schemas.solar import (
    SolarPositionRequest,
    SolarPositionResponse,
    DailyPositionsResponse,
)
from app.utils.logger import logger

router = APIRouter()


@router.get("/position", response_model=SolarPositionResponse)
async def get_solar_position(
    lat: float = Query(..., ge=-90, le=90, description="纬度"),
    lng: float = Query(..., ge=-180, le=180, description="经度"),
    date: Optional[str] = Query(None, description="日期 YYYY-MM-DD，默认当天"),
    hour: Optional[int] = Query(None, ge=0, le=23, description="小时(0-23)"),
    minute: Optional[int] = Query(0, ge=0, le=59, description="分钟(0-59)"),
    timezone: str = Query("Asia/Shanghai", description="时区"),
):
    """
    计算指定时间、地点的太阳位置

    返回太阳高度角、方位角、日出日落时间等
    """
    try:
        # 处理日期参数
        if date:
            try:
                target_date = datetime.strptime(date, "%Y-%m-%d").date()
            except ValueError:
                raise HTTPException(status_code=400, detail="日期格式错误，请使用 YYYY-MM-DD")
        else:
            target_date = datetime.now().date()

        # 处理时间参数
        if hour is None:
            now = datetime.now(pytz.timezone(timezone))
            hour = now.hour
            minute = now.minute

        logger.info(f"计算太阳位置: lat={lat}, lng={lng}, date={date}, time={hour}:{minute}")

        service = SolarService()

        # 计算太阳位置
        position = await service.calculate_solar_position(
            latitude=lat,
            longitude=lng,
            target_date=target_date,
            hour=hour,
            minute=minute,
            timezone=timezone,
        )

        return SolarPositionResponse(
            code=200,
            data=position,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"计算太阳位置失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"计算太阳位置失败: {str(e)}")


@router.get("/daily-positions", response_model=DailyPositionsResponse)
async def get_daily_positions(
    lat: float = Query(..., ge=-90, le=90, description="纬度"),
    lng: float = Query(..., ge=-180, le=180, description="经度"),
    date: Optional[str] = Query(None, description="日期 YYYY-MM-DD，默认当天"),
    timezone: str = Query("Asia/Shanghai", description="时区"),
):
    """
    获取24小时的太阳位置数据

    返回每小时太阳高度角和方位角
    """
    try:
        # 处理日期参数
        if date:
            try:
                target_date = datetime.strptime(date, "%Y-%m-%d").date()
            except ValueError:
                raise HTTPException(status_code=400, detail="日期格式错误，请使用 YYYY-MM-DD")
        else:
            target_date = datetime.now().date()

        logger.info(f"计算24小时太阳位置: lat={lat}, lng={lng}, date={date}")

        service = SolarService()

        # 计算24小时太阳位置
        positions = await service.calculate_daily_positions(
            latitude=lat,
            longitude=lng,
            target_date=target_date,
            timezone=timezone,
        )

        return DailyPositionsResponse(
            code=200,
            data={
                "date": target_date.isoformat(),
                "positions": positions,
            },
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"计算24小时太阳位置失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"计算24小时太阳位置失败: {str(e)}")


@router.get("/sunrise-sunset")
async def get_sunrise_sunset(
    lat: float = Query(..., ge=-90, le=90, description="纬度"),
    lng: float = Query(..., ge=-180, le=180, description="经度"),
    date: Optional[str] = Query(None, description="日期 YYYY-MM-DD，默认当天"),
    timezone: str = Query("Asia/Shanghai", description="时区"),
):
    """
    获取日出日落时间

    返回当天的日出、日落和日照时长
    """
    try:
        # 处理日期参数
        if date:
            try:
                target_date = datetime.strptime(date, "%Y-%m-%d").date()
            except ValueError:
                raise HTTPException(status_code=400, detail="日期格式错误，请使用 YYYY-MM-DD")
        else:
            target_date = datetime.now().date()

        logger.info(f"计算日出日落: lat={lat}, lng={lng}, date={date}")

        service = SolarService()

        # 计算日出日落
        sun_times = await service.calculate_sunrise_sunset(
            latitude=lat,
            longitude=lng,
            target_date=target_date,
            timezone=timezone,
        )

        return {
            "code": 200,
            "data": sun_times,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"计算日出日落失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"计算日出日落失败: {str(e)}")


@router.get("/key-dates")
async def get_key_dates_positions(
    lat: float = Query(..., ge=-90, le=90, description="纬度"),
    lng: float = Query(..., ge=-180, le=180, description="经度"),
    year: Optional[int] = Query(None, description="年份，默认当年"),
    hour: int = Query(12, ge=0, le=23, description="小时（默认正午12点）"),
):
    """
    获取关键日期的太阳位置

    包括：春分、夏至、秋分、冬至
    """
    try:
        if year is None:
            year = datetime.now().year

        logger.info(f"计算关键日期太阳位置: lat={lat}, lng={lng}, year={year}")

        service = SolarService()

        # 计算关键日期太阳位置
        key_positions = await service.calculate_key_dates_positions(
            latitude=lat,
            longitude=lng,
            year=year,
            hour=hour,
        )

        return {
            "code": 200,
            "data": key_positions,
        }

    except Exception as e:
        logger.error(f"计算关键日期太阳位置失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"计算关键日期太阳位置失败: {str(e)}")
