"""
SolarArc Pro - 配置管理模块
"""
from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """应用配置类"""

    # 应用基本信息
    APP_NAME: str = "SolarArc Pro"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = Field(default="development", pattern="^(development|production|testing)$")
    DEBUG: bool = False

    # 服务器配置
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    # 数据库配置
    DATABASE_URL: str = Field(
        default="mysql+pymysql://solararc:solararc_pass_2026@localhost:3306/solararc_pro?charset=utf8mb4"
    )
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 5
    DB_POOL_TIMEOUT: int = 30
    DB_POOL_RECYCLE: int = 3600

    # Redis配置
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_CACHE_TTL: int = 3600

    # CORS配置
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:8080,http://localhost:5173"
    CORS_METHODS: str = "GET,POST,PUT,DELETE,OPTIONS"
    CORS_HEADERS: str = "Content-Type,Authorization,X-Requested-With"

    # 安全配置
    SECRET_KEY: str = "your-secret-key-please-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # 日志配置
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "/app/logs/app.log"
    LOG_FILE_MAX_SIZE: int = 100  # MB
    LOG_FILE_BACKUP_COUNT: int = 10
    LOG_TO_CONSOLE: bool = True

    # 时区
    TZ: str = "Asia/Shanghai"

    # 地图API配置
    AMAP_API_KEY: str = ""
    TENCENT_MAP_API_KEY: str = ""
    BAIDU_MAP_API_KEY: str = ""

    # 坐标系配置
    DEFAULT_COORD_SYSTEM: str = Field(default="GCJ02", pattern="^(WGS84|GCJ02|BD09)$")
    AUTO_TRANSFORM_COORDS: bool = True

    # 文件上传配置
    MAX_UPLOAD_SIZE: int = 10485760  # 10MB
    ALLOWED_FILE_TYPES: str = ".geojson,.json,.shp,.kml,.csv"
    UPLOAD_DIR: str = "/app/uploads"

    # 缓存配置
    ENABLE_CACHE: bool = True
    DEFAULT_CACHE_TTL: int = 3600
    SOLAR_POSITION_CACHE_TTL: int = 86400  # 24小时
    SHADOW_CACHE_TTL: int = 604800  # 7天

    # 性能配置
    GUNICORN_WORKERS: int = 2
    GUNICORN_WORKER_CLASS: str = "uvicorn.workers.UvicornWorker"
    MAX_REQUESTS: int = 10000
    REQUEST_TIMEOUT: int = 60

    # 监控配置
    ENABLE_PERFORMANCE_MONITORING: bool = True
    ENABLE_REQUEST_LOGGING: bool = True
    SLOW_QUERY_THRESHOLD: float = 1.0

    # 中国城市数据配置
    DEFAULT_CITY: str = "北京"
    DEFAULT_CITY_CODE: str = "110000"
    CITY_DATA_FILE: str = "/app/data/cities.json"

    # 日照分析配置
    DACHAN_HAN_SOLSTICE_HOURS: int = 2
    DONGZHI_SOLSTICE_HOURS: int = 1
    SUNSHINE_ANALYSIS_STEP: int = 15  # 分钟

    # 导出配置
    EXPORT_TEMP_DIR: str = "/app/exports"
    EXPORT_FILE_TTL: int = 3600
    MAX_EXPORT_RECORDS: int = 10000

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

    @property
    def cors_origins_list(self) -> List[str]:
        """将CORS_ORIGINS字符串转换为列表"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]


# 全局配置实例
settings = Settings()
