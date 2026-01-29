"""
用户配置ORM模型

符合需求文档第4.2.4节的用户配置表设计
"""
import uuid
from sqlalchemy import Column, String, Numeric, SmallInteger, Date, DateTime, UniqueConstraint
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.sql import func
from app.core.database import Base


class UserSettings(Base):
    """用户配置表

    用于存储前端会话的地图状态和分析参数

    使用UUID作为主键，更适合分布式系统
    """
    __tablename__ = "user_settings"

    id = Column(
        CHAR(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        unique=True,
        nullable=False,
        comment="主键ID (UUID)"
    )
    session_id = Column(
        String(128),
        nullable=False,
        unique=True,
        comment="前端会话ID"
    )

    # 地图状态
    map_center_lat = Column(
        Numeric(10, 6),
        nullable=True,
        comment="地图中心纬度"
    )
    map_center_lng = Column(
        Numeric(10, 6),
        nullable=True,
        comment="地图中心经度"
    )
    map_zoom = Column(
        SmallInteger,
        nullable=True,
        comment="地图缩放级别"
    )

    # 分析参数
    analysis_date = Column(
        Date,
        nullable=True,
        comment="分析日期"
    )
    current_hour = Column(
        SmallInteger,
        nullable=True,
        comment="当前分析小时(0-23)"
    )

    # 时间戳
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        comment="更新时间"
    )

    def __repr__(self):
        return f"<UserSettings(session_id='{self.session_id}', zoom={self.map_zoom})>"
