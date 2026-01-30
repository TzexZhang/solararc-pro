"""
Shadow Analysis Models
"""
from sqlalchemy import Column, String, Integer, Numeric, DateTime, Date, ForeignKey
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.orm import relationship
from datetime import datetime
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


class ShadowAnalysisCache(Base):
    """Shadow analysis cache model"""

    __tablename__ = "shadow_analysis_cache"

    id = Column(VARCHAR(36), primary_key=True, default=generate_uuid, comment="缓存ID（UUID）")

    # Analysis parameters
    building_id = Column(VARCHAR(36), ForeignKey("buildings.id", ondelete="CASCADE"), nullable=False, index=True, comment="建筑ID")
    analysis_date = Column(Date, nullable=False, comment="分析日期")
    analysis_hour = Column(Integer, nullable=False, comment="分析小时")

    # Calculation results (stored as GeoJSON)
    shadow_polygon = Column(Polygon(srid=4326), nullable=False, comment="阴影多边形")
    shadow_area = Column(Numeric(15, 2), nullable=True, comment="阴影面积(平方米)")

    # Cache metadata
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    expires_at = Column(DateTime, nullable=False, index=True, comment="缓存过期时间")

    # Relationships
    building = relationship("Building", backref="shadow_analyses")

    def __repr__(self):
        return f"<ShadowAnalysisCache(id={self.id}, building_id={self.building_id}, date={self.analysis_date})>"
