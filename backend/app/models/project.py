"""
Project Models
"""
from sqlalchemy import Column, String, Integer, Numeric, DateTime, ForeignKey, Text, JSON
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.database import Base


def generate_uuid() -> str:
    """Generate UUID string"""
    return str(uuid.uuid4())


class Project(Base):
    """User project model"""

    __tablename__ = "projects"

    id = Column(VARCHAR(36), primary_key=True, default=generate_uuid, comment="项目ID（UUID）")
    user_id = Column(VARCHAR(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True, comment="用户ID")
    name = Column(VARCHAR(255), nullable=False, comment="项目名称")
    description = Column(Text, nullable=True, comment="项目描述")

    # Map center and zoom
    center_latitude = Column(Numeric(10, 7), nullable=False, comment="中心纬度")
    center_longitude = Column(Numeric(10, 7), nullable=False, comment="中心经度")
    zoom_level = Column(Integer, default=15, comment="缩放级别")

    # Configuration (JSON)
    config = Column(JSON, nullable=True, comment="配置参数")

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        comment="更新时间"
    )

    # Relationships
    user = relationship("User", back_populates="projects")
    analysis_reports = relationship("AnalysisReport", back_populates="project")

    def __repr__(self):
        return f"<Project(id={self.id}, name={self.name}, user_id={self.user_id})>"
