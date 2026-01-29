"""
建筑ORM模型
"""
import uuid
from sqlalchemy import Column, Integer, String, Numeric, DateTime, Text
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.sql import func
from geoalchemy2 import Geometry
from app.core.database import Base


class Building(Base):
    """建筑表

    符合需求文档第4.2.1节的建筑表设计

    使用UUID作为主键，更适合分布式系统
    """
    __tablename__ = "buildings"

    id = Column(
        CHAR(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        unique=True,
        nullable=False,
        comment="建筑ID (UUID)"
    )
    name = Column(String(255), nullable=True, comment="建筑名称")
    building_type = Column(
        String(50),
        nullable=True,
        comment="建筑类型 (residential/commercial/industrial/public)"
    )

    # 空间几何数据
    footprint = Column(
        Geometry('POLYGON', srid=4326, spatial_index=True),
        nullable=False,
        comment="建筑底面多边形 (WGS84)"
    )
    total_height = Column(
        Numeric(10, 2),
        nullable=False,
        comment="总高度(米)"
    )
    floor_area = Column(
        Numeric(15, 2),
        nullable=True,
        comment="楼层面积(平方米)"
    )
    floor_count = Column(Integer, nullable=True, comment="楼层数")

    # 光学属性
    reflective_rate = Column(
        Numeric(3, 2),
        default=0.30,
        comment="反射率(0-1)"
    )

    # 元数据
    address = Column(String(500), nullable=True, comment="地址")
    district = Column(String(100), nullable=True, comment="区域")
    city = Column(String(100), default="未知城市", comment="城市")
    country = Column(String(50), default="China", comment="国家")

    # 时间戳
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        comment="创建时间"
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        comment="更新时间"
    )

    def __repr__(self):
        return f"<Building(id={self.id}, name='{self.name}', city='{self.city}')>"
