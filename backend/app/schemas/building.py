"""
建筑相关的Schema定义
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any
from datetime import datetime


class BuildingBase(BaseModel):
    """建筑基础Schema"""
    name: Optional[str] = Field(None, description="建筑名称")
    building_type: Optional[str] = Field(None, description="建筑类型")
    total_height: float = Field(..., gt=0, description="建筑高度（米）")
    floor_area: Optional[float] = Field(None, gt=0, description="楼层面积（平方米）")
    floor_count: Optional[int] = Field(None, gt=0, description="楼层数")
    reflective_rate: Optional[float] = Field(0.3, ge=0, le=1, description="反射率")
    address: Optional[str] = Field(None, description="地址")
    district: Optional[str] = Field(None, description="区域")
    city: Optional[str] = Field("未知城市", description="城市")
    country: Optional[str] = Field("China", description="国家")


class BuildingCreate(BuildingBase):
    """创建建筑Schema"""
    footprint: Dict[str, Any] = Field(..., description="建筑底面多边形（GeoJSON格式）")


class BuildingUpdate(BaseModel):
    """更新建筑Schema"""
    name: Optional[str] = None
    building_type: Optional[str] = None
    total_height: Optional[float] = None
    floor_area: Optional[float] = None
    floor_count: Optional[int] = None
    reflective_rate: Optional[float] = None
    address: Optional[str] = None
    district: Optional[str] = None
    city: Optional[str] = None
    footprint: Optional[Dict[str, Any]] = None


class BuildingResponse(BaseModel):
    """建筑响应Schema"""
    code: int
    data: Optional[Dict[str, Any]] = None


class BuildingListResponse(BaseModel):
    """建筑列表响应Schema"""
    code: int
    data: Dict[str, Any]


class BBoxQuery(BaseModel):
    """Bounding Box查询Schema"""
    min_lat: float = Field(..., ge=-90, le=90)
    max_lat: float = Field(..., ge=-90, le=90)
    min_lng: float = Field(..., ge=-180, le=180)
    max_lng: float = Field(..., ge=-180, le=180)
    include_shadow: bool = False
    analysis_date: Optional[str] = None
    analysis_hour: Optional[int] = None
