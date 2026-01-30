"""
Solar Position Models
"""
from sqlalchemy import Column, String, Date, Integer, Numeric, DateTime, UniqueConstraint
from sqlalchemy.dialects.mysql import VARCHAR
from datetime import datetime
import uuid

from app.database import Base


def generate_uuid() -> str:
    """Generate UUID string"""
    return str(uuid.uuid4())


class SolarPositionPrecalc(Base):
    """Solar position pre-calculation model"""

    __tablename__ = "solar_positions_precalc"

    id = Column(VARCHAR(36), primary_key=True, default=generate_uuid, comment="记录ID（UUID）")

    # Location parameters
    latitude = Column(Numeric(10, 6), nullable=False, comment="纬度")
    longitude = Column(Numeric(10, 6), nullable=False, comment="经度")

    # Time parameters
    date = Column(Date, nullable=False, index=True, comment="日期")
    hour = Column(Integer, nullable=False, comment="小时(0-23)")

    # Solar position parameters
    altitude_angle = Column(Numeric(10, 6), nullable=False, comment="太阳高度角(度)")
    azimuth_angle = Column(Numeric(10, 6), nullable=False, comment="太阳方位角(度)")

    # Unique constraint
    __table_args__ = (
        UniqueConstraint('latitude', 'longitude', 'date', 'hour', name='idx_location_datetime'),
    )

    def __repr__(self):
        return f"<SolarPositionPrecalc(lat={self.latitude}, lng={self.longitude}, date={self.date}, hour={self.hour})>"
