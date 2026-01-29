"""
阴影分析缓存ORM模型

符合需求文档第4.2.3节的阴影分析记录表设计
"""
import uuid
from sqlalchemy import Column, String, Numeric, Date, SmallInteger, DateTime, ForeignKey, Index
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from app.core.database import Base


class ShadowAnalysisCache(Base):
    """阴影分析缓存表

    用于缓存阴影计算结果，避免重复计算

    使用UUID作为主键，更适合分布式系统
    """
    __tablename__ = "shadow_analysis_cache"

    id = Column(
        CHAR(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        unique=True,
        nullable=False,
        comment="主键ID (UUID)"
    )

    # 分析参数
    building_id = Column(
        CHAR(36),
        ForeignKey("buildings.id", ondelete="CASCADE"),
        nullable=False,
        comment="建筑ID (UUID)"
    )
    analysis_date = Column(
        Date,
        nullable=False,
        comment="分析日期"
    )
    analysis_hour = Column(
        SmallInteger,
        nullable=False,
        comment="分析小时(0-23)"
    )

    # 计算结果 (存储为空间几何数据)
    shadow_polygon = Column(
        Geometry('POLYGON', srid=4326, spatial_index=True),
        nullable=False,
        comment="阴影多边形"
    )
    shadow_area = Column(
        Numeric(15, 2),
        nullable=True,
        comment="阴影面积(平方米)"
    )

    # 缓存元数据
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        comment="创建时间"
    )
    expires_at = Column(
        DateTime(timezone=True),
        nullable=False,
        comment="缓存过期时间"
    )

    # 关系
    building = relationship("Building", backref="shadow_cache")

    # 索引
    __table_args__ = (
        Index('idx_building_datetime', 'building_id', 'analysis_date', 'analysis_hour'),
        Index('idx_expires', 'expires_at'),
    )

    def __repr__(self):
        return f"<ShadowAnalysisCache(id={self.id}, building_id={self.building_id}, date={self.analysis_date}, hour={self.analysis_hour})>"
