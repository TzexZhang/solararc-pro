"""
Analysis Schemas
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import date


class PointLocation(BaseModel):
    """Point location"""
    lat: float = Field(..., ge=-90, le=90)
    lng: float = Field(..., ge=-180, le=180)


class PointSunlightRequest(BaseModel):
    """Point sunlight analysis request"""
    point: PointLocation
    date: Optional[str] = Field(None, description="Date in YYYY-MM-DD format")
    start_hour: int = Field(6, ge=0, le=23)
    end_hour: int = Field(18, ge=0, le=23)


class HourlyBreakdown(BaseModel):
    """Hourly sunlight breakdown"""
    hour: int
    is_sunny: bool
    blocked_by: Optional[str] = None


class PointSunlightResponse(BaseModel):
    """Point sunlight analysis response"""
    total_hours: int
    sunlight_hours: float
    sunlight_rate: float
    hourly_breakdown: List[HourlyBreakdown]


class ShadowOverlapRequest(BaseModel):
    """Shadow overlap analysis request"""
    target_building_id: str
    surrounding_building_ids: List[str]
    date: Optional[str] = Field(None, description="Date in YYYY-MM-DD format")
    hour: int = Field(12, ge=0, le=23)


class OverlapDetail(BaseModel):
    """Overlap detail"""
    building_id: str
    overlap_area: float


class ShadowOverlapResponse(BaseModel):
    """Shadow overlap analysis response"""
    self_shadow_area: float
    projected_shadow_area: float
    overlap_area: float
    overlap_details: List[OverlapDetail]


class ShadowCalculationRequest(BaseModel):
    """Shadow calculation request"""
    building_ids: List[str]
    date: Optional[str] = Field(None, description="Date in YYYY-MM-DD format")
    hour: int = Field(12, ge=0, le=23)
    minute: int = Field(0, ge=0, le=59)


class ShadowPolygon(BaseModel):
    """Shadow polygon"""
    building_id: str
    shadow_polygon: Dict[str, Any]
    area: float


class ShadowCalculationResponse(BaseModel):
    """Shadow calculation response"""
    shadows: List[ShadowPolygon]
    calculation_time_ms: int


class ShadowPolygonData(BaseModel):
    """Shadow polygon data"""
    shadow_polygon: Dict[str, Any]
    shadow_length_coefficient: float


class ShadowComparisonResponse(BaseModel):
    """Shadow comparison response (winter vs summer solstice)"""
    winter_solstice: ShadowPolygonData
    summer_solstice: ShadowPolygonData
    ratio: float
