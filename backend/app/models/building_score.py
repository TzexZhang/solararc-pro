"""
Building Score Models
"""
from sqlalchemy import Column, String, Integer, Numeric, DateTime, ForeignKey, SQLEnum, JSON
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
import uuid

from app.database import Base


def generate_uuid() -> str:
    """Generate UUID string"""
    return str(uuid.uuid4())


class GradeType(str, enum.Enum):
    """Grade type enum"""
    EXCELLENT = "excellent"
    GOOD = "good"
    MODERATE = "moderate"
    POOR = "poor"


class BuildingScore(Base):
    """Building daylight score model"""

    __tablename__ = "building_scores"

    id = Column(VARCHAR(36), primary_key=True, default=generate_uuid, comment="评分ID（UUID）")
    report_id = Column(VARCHAR(36), ForeignKey("analysis_reports.id", ondelete="CASCADE"), nullable=False, index=True, comment="关联报告ID")
    building_id = Column(VARCHAR(36), nullable=False, index=True, comment="建筑ID")

    # Overall score
    overall_score = Column(Integer, nullable=False, index=True, comment="综合评分（0-100）")
    grade = Column(SQLEnum(GradeType), nullable=False, comment="等级")

    # Detailed metrics
    avg_sunlight_hours = Column(Numeric(10, 2), nullable=True, comment="平均日照时长")
    peak_sunlight_hours = Column(Numeric(10, 2), nullable=True, comment="峰值日照时长")
    continuous_sunlight_hours = Column(Numeric(10, 2), nullable=True, comment="最长连续日照时长")
    shadow_frequency = Column(Integer, nullable=True, comment="被遮挡频次")

    # Shading buildings (JSON)
    shading_buildings = Column(JSON, nullable=True, comment="遮挡源建筑ID列表")

    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")

    # Relationships
    report = relationship("AnalysisReport", back_populates="building_scores")

    def __repr__(self):
        return f"<BuildingScore(id={self.id}, building_id={self.building_id}, score={self.overall_score})>"
