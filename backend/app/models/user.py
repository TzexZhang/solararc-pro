"""
User Models
"""
from sqlalchemy import Column, String, Boolean, Integer, DateTime, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import VARCHAR
from datetime import datetime
import enum
import uuid

from app.database import Base


def generate_uuid() -> str:
    """Generate UUID string"""
    return str(uuid.uuid4())


class LockReason(str, enum.Enum):
    """Account lock reason enum"""
    TOO_MANY_FAILED_ATTEMPTS = "too_many_failed_attempts"


class User(Base):
    """User model"""

    __tablename__ = "users"

    id = Column(VARCHAR(36), primary_key=True, default=generate_uuid, comment="用户ID（UUID）")
    email = Column(VARCHAR(255), unique=True, nullable=False, index=True, comment="邮箱（登录账号）")
    password_hash = Column(VARCHAR(255), nullable=False, comment="密码哈希（bcrypt）")
    nickname = Column(VARCHAR(50), nullable=True, comment="用户昵称")

    # Account status
    is_active = Column(Boolean, default=True, index=True, comment="账户是否激活")
    is_locked = Column(Boolean, default=False, comment="账户是否锁定")
    failed_login_count = Column(Integer, default=0, comment="失败登录次数")
    locked_until = Column(DateTime, nullable=True, comment="锁定到期时间")

    # Login information
    last_login_at = Column(DateTime, nullable=True, comment="最后登录时间")
    last_login_ip = Column(VARCHAR(45), nullable=True, comment="最后登录IP")

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        comment="更新时间"
    )

    # Relationships
    password_resets = relationship("PasswordReset", back_populates="user", cascade="all, delete-orphan", foreign_keys="PasswordReset.user_id")
    projects = relationship("Project", back_populates="user", cascade="all, delete-orphan")
    analysis_reports = relationship("AnalysisReport", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"


class PasswordReset(Base):
    """Password reset model"""

    __tablename__ = "password_resets"

    id = Column(VARCHAR(36), primary_key=True, default=generate_uuid, comment="重置ID（UUID）")
    user_id = Column(VARCHAR(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True, comment="用户ID")
    token = Column(VARCHAR(255), unique=True, nullable=False, index=True, comment="重置令牌")
    expires_at = Column(DateTime, nullable=False, index=True, comment="过期时间")
    used = Column(Boolean, default=False, comment="是否已使用")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")

    # Relationships
    user = relationship("User", back_populates="password_resets")

    def __repr__(self):
        return f"<PasswordReset(id={self.id}, user_id={self.user_id})>"
