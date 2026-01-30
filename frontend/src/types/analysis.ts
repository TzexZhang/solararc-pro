import { AnalysisType, Coordinate, LatLng, ExportFormat } from './common'

// Solar Position
export interface SolarPosition {
  solar_altitude: number // degrees
  solar_azimuth: number // degrees
  sunrise_time: string // HH:MM:SS
  sunset_time: string // HH:MM:SS
  day_length: number // hours
  timestamp: string
}

export interface SolarPositionParams {
  lat: number
  lng: number
  date?: string // YYYY-MM-DD
  hour?: number // 0-23
  minute?: number // 0-59
  timezone?: string
}

export interface DailySolarPosition {
  date: string
  positions: HourlySolarPosition[]
}

export interface HourlySolarPosition {
  hour: number
  altitude: number
  azimuth: number
}

// Shadow Calculation
export interface ShadowCalculateParams {
  building_ids: string[]
  date: string // YYYY-MM-DD
  hour: number // 0-23
  minute?: number // 0-59
}

export interface ShadowResult {
  building_id: string
  shadow_polygon: GeoJSON.Polygon
  area: number
}

export interface ShadowCalculateResponse {
  shadows: ShadowResult[]
  calculation_time_ms: number
}

export interface ShadowCompareExtremes {
  winter_solstice: {
    date: string
    shadow_polygon: GeoJSON.Polygon
    shadow_length_coefficient: number
  }
  summer_solstice: {
    date: string
    shadow_polygon: GeoJSON.Polygon
    shadow_length_coefficient: number
  }
  ratio: number
}

// Sunlight Analysis
export interface PointSunlightParams {
  point: LatLng
  date: string
  start_hour?: number
  end_hour?: number
}

export interface HourlySunlight {
  hour: number
  is_sunny: boolean
  blocked_by?: string
}

export interface PointSunlightResponse {
  total_hours: number
  sunlight_hours: number
  sunlight_rate: number
  hourly_breakdown: HourlySunlight[]
}

export interface ShadowOverlapParams {
  target_building_id: string
  surrounding_building_ids: string[]
  date: string
  hour: number
}

export interface ShadowOverlapDetail {
  building_id: string
  overlap_area: number
}

export interface ShadowOverlapResponse {
  self_shadow_area: number
  projected_shadow_area: number
  overlap_area: number
  overlap_details: ShadowOverlapDetail[]
}

// Analysis Reports
export interface CreateReportParams {
  project_id?: string
  name: string
  analysis_type: AnalysisType
  latitude: number
  longitude: number
  date_start: string
  date_end: string
  building_ids: string[]
}

export interface AnalysisReport {
  id: string
  user_id: string
  project_id?: string
  name: string
  analysis_type: AnalysisType
  latitude: number
  longitude: number
  date_start: string
  date_end: string
  total_sunlight_hours?: number
  avg_shadow_coverage?: number
  building_count?: number
  results: ReportResults
  report_file_path?: string
  status: 'processing' | 'completed' | 'failed'
  created_at: string
  updated_at: string
}

export interface ReportResults {
  hourly_sunlight?: number[]
  sun_path_data?: SunPathData[]
  shadow_heatmap?: HeatmapData[]
  building_scores?: BuildingScore[]
}

export interface SunPathData {
  hour: number
  altitude: number
  azimuth: number
}

export interface HeatmapData {
  lat: number
  lng: number
  value: number
}

export interface BuildingScore {
  building_id: string
  building_name?: string
  overall_score: number // 0-100
  grade: 'excellent' | 'good' | 'moderate' | 'poor'
  avg_sunlight_hours: number
  peak_sunlight_hours: number
  continuous_sunlight_hours: number
  shadow_frequency: number
  shading_buildings: string[]
}

export interface ReportListParams {
  page?: number
  page_size?: number
  project_id?: string
}

export interface ReportListResponse {
  total: number
  page: number
  page_size: number
  reports: AnalysisReport[]
}

export interface ChartData {
  chart_type: string
  data: {
    x_axis?: any[]
    series?: ChartSeries[]
    [key: string]: any
  }
}

export interface ChartSeries {
  name: string
  data: number[]
  color?: string
}

export interface ExportReportParams {
  format: ExportFormat
}
