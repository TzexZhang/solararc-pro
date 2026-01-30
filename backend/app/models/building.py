"""
Building Models
"""
from sqlalchemy import Column, String, Integer, Numeric, DateTime, Text, Enum as SQLEnum
from sqlalchemy.dialects.mysql import VARCHAR
from datetime import datetime
import enum
import uuid

from app.database import Base

# Import geoalchemy2 elements
try:
    from geoalchemy2.elements import Polygon
except ImportError:
    try:
        from geoalchemy2.types import Polygon
    except ImportError:
        # Last resort - import Geometry and use as Polygon
        from geoalchemy2 import Geometry
        Polygon = Geometry


def generate_uuid() -> str:
    """Generate UUID string"""
    return str(uuid.uuid4())


class BuildingType(str, enum.Enum):
    """Building type enum"""
    RESIDENTIAL = "residential"
    COMMERCIAL = "commercial"
    INDUSTRIAL = "industrial"
    PUBLIC = "public"


class Building(Base):
    """Building model"""

    __tablename__ = "buildings"

    id = Column(VARCHAR(36), primary_key=True, default=generate_uuid, comment="建筑ID（UUID）")
    name = Column(VARCHAR(255), nullable=True, comment="建筑名称")
    building_type = Column(
        SQLEnum(BuildingType),
        nullable=True,
        comment="建筑类型"
    )

    # Spatial geometry data
    footprint = Column(Polygon(srid=4326), nullable=False, comment="建筑底面多边形 (WGS84)")
    total_height = Column(Numeric(10, 2), nullable=False, comment="总高度(米)")
    floor_area = Column(Numeric(15, 2), nullable=True, comment="楼层面积(平方米)")
    floor_count = Column(Integer, nullable=True, comment="楼层数")

    # Optical properties
    reflective_rate = Column(Numeric(3, 2), default=0.30, comment="反射率(0-1)")

    # Metadata
    address = Column(VARCHAR(500), nullable=True, comment="地址")
    district = Column(VARCHAR(100), nullable=True, comment="区域")
    city = Column(VARCHAR(100), default="未知城市", comment="城市")
    country = Column(VARCHAR(50), default="China", comment="国家")

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        comment="更新时间"
    )

    def __repr__(self):
        return f"<Building(id={self.id}, name={self.name}, height={self.total_height})>"
