"""
Application Configuration
"""
from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings"""

    # Database
    database_url: str = Field(
        default="mysql+pymysql://root:password@localhost:3306/solararc_pro",
        description="Database connection URL"
    )
    db_pool_size: int = Field(default=10, description="Database connection pool size")
    db_max_overflow: int = Field(default=5, description="Database connection pool max overflow")

    # API
    api_host: str = Field(default="127.0.0.1", description="API host")
    api_port: int = Field(default=8000, description="API port")
    api_v1_prefix: str = Field(default="/api/v1", description="API v1 prefix")

    # CORS
    cors_origins: str = Field(
        default="http://localhost:5173,http://localhost:3000",
        description="Comma-separated list of allowed CORS origins"
    )

    # Security
    secret_key: str = Field(
        default="your-secret-key-here",
        description="Secret key for JWT token generation"
    )
    algorithm: str = Field(default="HS256", description="JWT algorithm")
    access_token_expire_minutes: int = Field(
        default=10080,  # 7 days
        description="Access token expiration time in minutes"
    )

    # Map
    amap_api_key: str = Field(default="", description="Amap API key")

    # Timezone
    tz: str = Field(default="Asia/Shanghai", description="Timezone")

    # Logging
    log_level: str = Field(default="INFO", description="Log level")
    log_format: str = Field(default="json", description="Log format")

    # Environment
    environment: str = Field(default="development", description="Environment (development/production)")

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins string to list"""
        return [origin.strip() for origin in self.cors_origins.split(",")]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()
