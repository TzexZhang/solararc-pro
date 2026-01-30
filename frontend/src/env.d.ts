/// <reference types="vite/client" />

interface ImportMetaEnv {
  // ============================================
  // 应用配置
  // ============================================
  readonly VITE_APP_NAME: string
  readonly VITE_APP_VERSION: string
  readonly VITE_APP_DESCRIPTION: string
  readonly VITE_APP_ENV: 'development' | 'production'

  // ============================================
  // API 配置
  // ============================================
  readonly VITE_API_BASE_URL: string
  readonly VITE_API_TIMEOUT: number

  // ============================================
  // 地图配置
  // ============================================
  readonly VITE_MAPBOX_ACCESS_TOKEN: string
  readonly VITE_AMAP_API_KEY: string
  readonly VITE_MAP_CENTER_LAT: number
  readonly VITE_MAP_CENTER_LNG: number
  readonly VITE_MAP_DEFAULT_ZOOM: number

  // ============================================
  // 默认城市配置
  // ============================================
  readonly VITE_DEFAULT_CITY: string
  readonly VITE_DEFAULT_CITY_CODE: string
  readonly VITE_DEFAULT_TIMEZONE: string

  // ============================================
  // 功能开关
  // ============================================
  readonly VITE_ENABLE_ANALYSIS: string
  readonly VITE_ENABLE_EXPORT: string
  readonly VITE_ENABLE_PWA: string
  readonly VITE_ENABLE_3D_BUILDINGS: string
  readonly VITE_ENABLE_SHADOW_ANALYSIS: string

  // ============================================
  // 导出配置
  // ============================================
  readonly VITE_EXPORT_PDF_ENABLED: string
  readonly VITE_EXPORT_EXCEL_ENABLED: string
  readonly VITE_EXPORT_CSV_ENABLED: string

  // ============================================
  // 性能配置
  // ============================================
  readonly VITE_BUILDING_CACHE_TTL: number
  readonly VITE_SHADOW_CACHE_TTL: number
  readonly VITE_MAX_BUILDINGS_LOAD: number
  readonly VITE_DEFAULT_PAGE_SIZE: number

  // ============================================
  // 上传配置
  // ============================================
  readonly VITE_MAX_FILE_SIZE: number
  readonly VITE_ALLOWED_FILE_TYPES: string

  // ============================================
  // 开发工具配置
  // ============================================
  readonly VITE_DEV_TOOLS?: string
  readonly VITE_SHOW_SOURCE_MAP?: string
  readonly VITE_LOG_LEVEL?: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
