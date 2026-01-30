/**
 * 应用环境变量配置
 *
 * 所有环境变量从 import.meta.env 读取
 * Vite 会在构建时替换以 VITE_ 开头的变量
 */

// 应用配置
export const APP_NAME = import.meta.env.VITE_APP_NAME || 'SolarArc Pro'
export const APP_VERSION = import.meta.env.VITE_APP_VERSION || '1.0.0'
export const APP_DESCRIPTION = import.meta.env.VITE_APP_DESCRIPTION || 'High-performance urban solar analysis platform'
export const APP_ENV = import.meta.env.VITE_APP_ENV || (import.meta.env.DEV ? 'development' : 'production')

// API 配置
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api/v1'
export const API_TIMEOUT = Number(import.meta.env.VITE_API_TIMEOUT) || 30000

// 地图配置
export const MAPBOX_ACCESS_TOKEN = import.meta.env.VITE_MAPBOX_ACCESS_TOKEN || ''
export const AMAP_API_KEY = import.meta.env.VITE_AMAP_API_KEY || ''
export const MAP_CENTER = {
  lat: Number(import.meta.env.VITE_MAP_CENTER_LAT) || 39.9042,
  lng: Number(import.meta.env.VITE_MAP_CENTER_LNG) || 116.4074
}
export const MAP_DEFAULT_ZOOM = Number(import.meta.env.VITE_MAP_DEFAULT_ZOOM) || 15

// 默认城市配置
export const DEFAULT_CITY = import.meta.env.VITE_DEFAULT_CITY || '北京'
export const DEFAULT_CITY_CODE = import.meta.env.VITE_DEFAULT_CITY_CODE || '110000'
export const DEFAULT_TIMEZONE = import.meta.env.VITE_DEFAULT_TIMEZONE || 'Asia/Shanghai'

// 功能开关
export const ENABLE_ANALYSIS = import.meta.env.VITE_ENABLE_ANALYSIS === 'true'
export const ENABLE_EXPORT = import.meta.env.VITE_ENABLE_EXPORT === 'true'
export const ENABLE_PWA = import.meta.env.VITE_ENABLE_PWA === 'true'
export const ENABLE_3D_BUILDINGS = import.meta.env.VITE_ENABLE_3D_BUILDINGS === 'true'
export const ENABLE_SHADOW_ANALYSIS = import.meta.env.VITE_ENABLE_SHADOW_ANALYSIS === 'true'

// 导出配置
export const EXPORT_PDF_ENABLED = import.meta.env.VITE_EXPORT_PDF_ENABLED === 'true'
export const EXPORT_EXCEL_ENABLED = import.meta.env.VITE_EXPORT_EXCEL_ENABLED === 'true'
export const EXPORT_CSV_ENABLED = import.meta.env.VITE_EXPORT_CSV_ENABLED === 'true'

// 性能配置
export const BUILDING_CACHE_TTL = Number(import.meta.env.VITE_BUILDING_CACHE_TTL) || 300000
export const SHADOW_CACHE_TTL = Number(import.meta.env.VITE_SHADOW_CACHE_TTL) || 600000
export const MAX_BUILDINGS_LOAD = Number(import.meta.env.VITE_MAX_BUILDINGS_LOAD) || 1000
export const DEFAULT_PAGE_SIZE = Number(import.meta.env.VITE_DEFAULT_PAGE_SIZE) || 20

// 上传配置
export const MAX_FILE_SIZE = Number(import.meta.env.VITE_MAX_FILE_SIZE) || 10485760 // 10MB
export const ALLOWED_FILE_TYPES = (import.meta.env.VITE_ALLOWED_FILE_TYPES || '.jpg,.jpeg,.png,.pdf,.geojson,.json').split(',')

// 开发工具配置
export const DEV_TOOLS = import.meta.env.VITE_DEV_TOOLS === 'true'
export const SHOW_SOURCE_MAP = import.meta.env.VITE_SHOW_SOURCE_MAP === 'true'
export const LOG_LEVEL = import.meta.env.VITE_LOG_LEVEL || 'info'

/**
 * 判断是否为开发环境
 */
export const isDev = import.meta.env.DEV

/**
 * 判断是否为生产环境
 */
export const isProd = import.meta.env.PROD

/**
 * 判断是否启用某个功能
 */
export function isFeatureEnabled(feature: string): boolean {
  const envVar = import.meta.env[`VITE_ENABLE_${feature.toUpperCase()}`]
  return envVar === 'true'
}

export default {
  APP_NAME,
  APP_VERSION,
  APP_DESCRIPTION,
  APP_ENV,
  API_BASE_URL,
  API_TIMEOUT,
  MAPBOX_ACCESS_TOKEN,
  AMAP_API_KEY,
  MAP_CENTER,
  MAP_DEFAULT_ZOOM,
  DEFAULT_CITY,
  DEFAULT_CITY_CODE,
  DEFAULT_TIMEZONE,
  ENABLE_ANALYSIS,
  ENABLE_EXPORT,
  ENABLE_PWA,
  ENABLE_3D_BUILDINGS,
  ENABLE_SHADOW_ANALYSIS,
  EXPORT_PDF_ENABLED,
  EXPORT_EXCEL_ENABLED,
  EXPORT_CSV_ENABLED,
  BUILDING_CACHE_TTL,
  SHADOW_CACHE_TTL,
  MAX_BUILDINGS_LOAD,
  DEFAULT_PAGE_SIZE,
  MAX_FILE_SIZE,
  ALLOWED_FILE_TYPES,
  DEV_TOOLS,
  SHOW_SOURCE_MAP,
  LOG_LEVEL,
  isDev,
  isProd,
  isFeatureEnabled
}
