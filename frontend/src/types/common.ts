// Common types

export interface ApiResponse<T = any> {
  code: number
  message?: string
  data: T
}

export interface ApiError {
  code: number
  error: string
  message: string
  details?: Record<string, any>
}

export interface PaginationParams {
  page?: number
  page_size?: number
}

export interface PaginationResponse<T> {
  total: number
  page: number
  page_size: number
  items: T[]
}

export type Coordinate = [number, number] // [longitude, latitude]

export interface LatLng {
  lat: number
  lng: number
}

export interface Bounds {
  minLat: number
  maxLat: number
  minLng: number
  maxLng: number
}

export enum BuildingType {
  RESIDENTIAL = 'residential',
  COMMERCIAL = 'commercial',
  INDUSTRIAL = 'industrial',
  PUBLIC = 'public'
}

export enum AnalysisType {
  DAILY = 'daily',
  SEASONAL = 'seasonal',
  CUSTOM = 'custom'
}

export enum ViewMode {
  MAP = 'map',
  WHITE_MODEL = 'white-model',
  HYBRID = 'hybrid'
}

export enum ExportFormat {
  PDF = 'pdf',
  EXCEL = 'excel',
  CSV = 'csv',
  GEOJSON = 'geojson'
}
