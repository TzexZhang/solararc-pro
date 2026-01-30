"""
Solar Position Schemas
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class SolarPositionRequest(BaseModel):
    """Solar position calculation request"""
    lat: float = Field(..., ge=-90, le=90, description="Latitude")
    lng: float = Field(..., ge=-180, le=180, description="Longitude")
    date: Optional[str] = Field(None, description="Date in YYYY-MM-DD format")
    hour: Optional[int] = Field(None, ge=0, le=23, description="Hour (0-23)")
    minute: Optional[int] = Field(0, ge=0, le=59, description="Minute (0-59)")
    timezone: Optional[str] = Field("Asia/Shanghai", description="Timezone")


class SolarHourlyPosition(BaseModel):
    """Hourly solar position"""
    hour: int
    altitude: float = Field(..., description="Solar altitude angle in degrees")
    azimuth: float = Field(..., description="Solar azimuth angle in degrees")


class SolarPositionResponse(BaseModel):
    """Solar position response"""
    solar_altitude: float = Field(..., description="Solar altitude angle in degrees")
    solar_azimuth: float = Field(..., description="Solar azimuth angle in degrees")
    sunrise_time: Optional[str] = Field(None, description="Sunrise time")
    sunset_time: Optional[str] = Field(None, description="Sunset time")
    day_length: Optional[float] = Field(None, description="Day length in hours")
    timestamp: str


class SolarDailyPositionsRequest(BaseModel):
    """Daily solar positions request"""
    lat: float = Field(..., ge=-90, le=90, description="Latitude")
    lng: float = Field(..., ge=-180, le=180, description="Longitude")
    date: Optional[str] = Field(None, description="Date in YYYY-MM-DD format")


class SolarDailyPositionsResponse(BaseModel):
    """Daily solar positions response"""
    date: str
    positions: List[SolarHourlyPosition]
