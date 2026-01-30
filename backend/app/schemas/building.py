"""
Building Schemas
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum


class BuildingType(str, Enum):
    """Building type enum"""
    RESIDENTIAL = "residential"
    COMMERCIAL = "commercial"
    INDUSTRIAL = "industrial"
    PUBLIC = "public"


class BuildingBase(BaseModel):
    """Base building schema"""
    name: Optional[str] = Field(None, max_length=255)
    building_type: Optional[BuildingType] = None
    total_height: float = Field(..., gt=0)
    floor_area: Optional[float] = Field(None, gt=0)
    floor_count: Optional[int] = Field(None, gt=0)
    reflective_rate: float = Field(default=0.3, ge=0, le=1)
    address: Optional[str] = None
    district: Optional[str] = None
    city: str = Field(default="未知城市", max_length=100)
    country: str = Field(default="China", max_length=50)


class BuildingCreate(BuildingBase):
    """Building creation schema"""
    footprint: Dict[str, Any] = Field(..., description="GeoJSON Polygon")


class BuildingUpdate(BaseModel):
    """Building update schema"""
    name: Optional[str] = Field(None, max_length=255)
    building_type: Optional[BuildingType] = None
    total_height: Optional[float] = Field(None, gt=0)
    floor_area: Optional[float] = Field(None, gt=0)
    floor_count: Optional[int] = Field(None, gt=0)
    reflective_rate: Optional[float] = Field(None, ge=0, le=1)
    address: Optional[str] = None
    district: Optional[str] = None
    city: Optional[str] = None
    footprint: Optional[Dict[str, Any]] = None


class BuildingResponse(BaseModel):
    """Building response schema"""
    id: str
    name: Optional[str] = None
    building_type: Optional[BuildingType] = None
    footprint: Dict[str, Any]
    total_height: float
    floor_area: Optional[float] = None
    floor_count: Optional[int] = None
    reflective_rate: float
    address: Optional[str] = None
    district: Optional[str] = None
    city: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class BuildingListResponse(BaseModel):
    """Building list response schema"""
    buildings: list[BuildingResponse]
    total: int
