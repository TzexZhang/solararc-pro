"""
Solar Position Calculation API Routes
"""
from fastapi import APIRouter, Query
from typing import Optional

from app.schemas.solar import (
    SolarPositionRequest,
    SolarPositionResponse,
    SolarDailyPositionsRequest,
    SolarDailyPositionsResponse
)
from app.services.solar_service import (
    calculate_solar_position,
    calculate_daily_solar_positions
)

router = APIRouter(prefix="/solar", tags=["Solar Position"])


@router.get("/position", response_model=dict)
async def get_solar_position(
    lat: float = Query(..., ge=-90, le=90, description="Latitude in degrees"),
    lng: float = Query(..., ge=-180, le=180, description="Longitude in degrees"),
    date: Optional[str] = Query(None, description="Date in YYYY-MM-DD format"),
    hour: Optional[int] = Query(None, ge=0, le=23, description="Hour (0-23)"),
    minute: Optional[int] = Query(0, ge=0, le=59, description="Minute (0-59)"),
    timezone: Optional[str] = Query("Asia/Shanghai", description="Timezone")
):
    """
    Calculate solar position (altitude and azimuth angles) for a given location and time

    - **lat**: Latitude (-90 to 90)
    - **lng**: Longitude (-180 to 180)
    - **date**: Date in YYYY-MM-DD format (default: today)
    - **hour**: Hour (0-23, default: current hour)
    - **minute**: Minute (0-59, default: 0)
    - **timezone**: Timezone string (default: Asia/Shanghai)

    Returns solar altitude angle, solar azimuth angle, sunrise/sunset times
    """
    result = calculate_solar_position(lat, lng, date, hour, minute, timezone)

    return {
        "code": 200,
        "data": result
    }


@router.get("/daily-positions", response_model=dict)
async def get_daily_solar_positions(
    lat: float = Query(..., ge=-90, le=90, description="Latitude in degrees"),
    lng: float = Query(..., ge=-180, le=180, description="Longitude in degrees"),
    date: Optional[str] = Query(None, description="Date in YYYY-MM-DD format"),
    timezone: Optional[str] = Query("Asia/Shanghai", description="Timezone")
):
    """
    Calculate solar positions for all 24 hours of a day

    - **lat**: Latitude (-90 to 90)
    - **lng**: Longitude (-180 to 180)
    - **date**: Date in YYYY-MM-DD format (default: today)
    - **timezone**: Timezone string (default: Asia/Shanghai)

    Returns hourly solar positions including altitude and azimuth angles
    """
    result = calculate_daily_solar_positions(lat, lng, date, timezone)

    return {
        "code": 200,
        "data": result
    }
