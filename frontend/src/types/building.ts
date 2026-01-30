import { BuildingType, Coordinate } from './common'

export interface Building {
  id: string
  name?: string
  building_type: BuildingType

  // Geometry
  footprint: GeoJSON.Polygon
  height: number // meters
  floor_area?: number // square meters
  floor_count?: number

  // Optical properties
  reflective_rate?: number // 0-1

  // Metadata
  address?: string
  district?: string
  city?: string
  country?: string

  // Analysis data (optional)
  shadow?: ShadowData
  sunlight_stats?: SunlightStats

  created_at: string
  updated_at: string
}

export interface ShadowData {
  polygon: GeoJSON.Polygon
  area: number
  shadow_length_coefficient?: number
}

export interface SunlightStats {
  total_hours: number
  sunlight_hours: number
  sunlight_rate: number
  avg_daily_hours: number
  peak_hours: number
}

export interface BuildingImportParams {
  file: File
  city?: string
}

export interface BuildingImportResult {
  success_count: number
  failed_count: number
  errors: string[]
}

export interface BuildingQueryParams {
  min_lat: number
  max_lat: number
  min_lng: number
  max_lng: number
  include_shadow?: boolean
  analysis_date?: string
  analysis_hour?: number
}

export interface BuildingListResponse {
  buildings: Building[]
  total: number
}
