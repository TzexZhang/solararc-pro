"""
太阳位置预计算ORM模型

符合需求文档第4.2.2节的太阳位置预计算表设计
"""
import uuid
from sqlalchemy import Column, String, Numeric, Date, SmallInteger, DateTime, UniqueConstraint, Index
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.sql import func
from app.core.database import Base


class SolarPositionPrecalc(Base):
    """太阳位置预计算表

    用于存储关键日期的太阳位置数据，优化查询性能
    仅预计算关键日期: 春分、夏至、秋分、冬至

    使用UUID作为主键，更适合分布式系统
    """
    __tablename__ = "solar_positions_precalc"

    id = Column(
        CHAR(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        unique=True,
        nullable=False,
        comment="主键ID (UUID)"
    )

    # 位置参数
    latitude = Column(
        Numeric(10, 6),
        nullable=False,
        comment="纬度"
    )
    longitude = Column(
        Numeric(10, 6),
        nullable=False,
        comment="经度"
    )

    # 时间参数
    date = Column(
        Date,
        nullable=False,
        comment="日期"
    )
    hour = Column(
        SmallInteger,
        nullable=False,
        comment="小时(0-23)"
    )

    # 太阳位置参数
    altitude_angle = Column(
        Numeric(10, 6),
        nullable=False,
        comment="太阳高度角(度)"
    )
    azimuth_angle = Column(
        Numeric(10, 6),
        nullable=False,
        comment="太阳方位角(度)"
    )

    # 元数据
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        comment="创建时间"
    )

    # 约束和索引
    __table_args__ = (
        UniqueConstraint(
            'latitude', 'longitude', 'date', 'hour',
            name='idx_location_datetime'
        ),
        Index('idx_date', 'date'),
    )

    def __repr__(self):
        return f"<SolarPositionPrecalc(lat={self.latitude}, lng={self.longitude}, date={self.date}, hour={self.hour})>"
