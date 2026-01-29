"""
太阳相关的Schema定义
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class SolarPositionResponse(BaseModel):
    """太阳位置响应Schema"""
    code: int
    data: Optional[Dict[str, Any]] = None


class DailyPositionsResponse(BaseModel):
    """每日太阳位置响应Schema"""
    code: int
    data: Optional[Dict[str, Any]] = None
