"""
Analysis Report Models
"""
from sqlalchemy import Column, String, Date, Integer, Numeric, DateTime, ForeignKey, Text, JSON, SQLEnum
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
import uuid

from app.database import Base


def generate_uuid() -> str:
    """Generate UUID string"""
    return str(uuid.uuid4())


class AnalysisType(str, enum.Enum):
    """Analysis type enum"""
    DAILY = "daily"
    SEASONAL = "seasonal"
    CUSTOM = "custom"


class AnalysisReport(Base):
    """Analysis report model"""

    __tablename__ = "analysis_reports"

    id = Column(VARCHAR(36), primary_key=True, default=generate_uuid, comment="报告ID（UUID）")
    user_id = Column(VARCHAR(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True, comment="用户ID")
    project_id = Column(VARCHAR(36), ForeignKey("projects.id", ondelete="SET NULL"), nullable=True, index=True, comment="关联项目ID")
    name = Column(VARCHAR(255), nullable=False, comment="报告名称")
    analysis_type = Column(SQLEnum(AnalysisType), nullable=False, comment="分析类型")

    # Location and time range
    latitude = Column(Numeric(10, 7), nullable=False, comment="分析中心纬度")
    longitude = Column(Numeric(10, 7), nullable=False, comment="分析中心经度")
    date_start = Column(Date, nullable=False, comment="分析开始日期")
    date_end = Column(Date, nullable=False, comment="分析结束日期")

    # Analysis results
    total_sunlight_hours = Column(Numeric(10, 2), nullable=True, comment="总日照时长")
    avg_shadow_coverage = Column(Numeric(5, 2), nullable=True, comment="平均阴影覆盖率（%）")
    building_count = Column(Integer, nullable=True, comment="分析建筑数量")
    results = Column(JSON, nullable=False, comment="详细分析结果（图表数据）")

    # Report file
    report_file_path = Column(VARCHAR(500), nullable=True, comment="PDF报告文件路径")

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True, comment="创建时间")
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        comment="更新时间"
    )

    # Relationships
    user = relationship("User", back_populates="analysis_reports")
    project = relationship("Project", back_populates="analysis_reports")
    building_scores = relationship("BuildingScore", back_populates="report", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<AnalysisReport(id={self.id}, name={self.name}, type={self.analysis_type})>"
