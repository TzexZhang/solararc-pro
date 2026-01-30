import { http } from '@/utils/request'
import type {
  PointSunlightParams,
  PointSunlightResponse,
  ShadowOverlapParams,
  ShadowOverlapResponse,
  CreateReportParams,
  AnalysisReport,
  ReportListParams,
  ReportListResponse,
  ChartData
} from '@/types'

/**
 * Sunlight Analysis API
 */
export const analysisService = {
  /**
   * Analyze sunlight at a specific point
   */
  async analyzePointSunlight(params: PointSunlightParams): Promise<PointSunlightResponse> {
    return http.post<PointSunlightResponse>('/analysis/point-sunlight', params)
  },

  /**
   * Analyze shadow overlap between buildings
   */
  async analyzeShadowOverlap(params: ShadowOverlapParams): Promise<ShadowOverlapResponse> {
    return http.post<ShadowOverlapResponse>('/analysis/shadow-overlap', params)
  },

  /**
   * Create analysis report
   */
  async createReport(params: CreateReportParams): Promise<AnalysisReport> {
    return http.post<AnalysisReport>('/analysis/reports', params)
  },

  /**
   * Get analysis reports list
   */
  async getReports(params?: ReportListParams): Promise<ReportListResponse> {
    return http.get<ReportListResponse>('/analysis/reports', { params })
  },

  /**
   * Get single report by ID
   */
  async getReportById(reportId: string): Promise<AnalysisReport> {
    return http.get<AnalysisReport>(`/analysis/reports/${reportId}`)
  },

  /**
   * Get building scores for a report
   */
  async getBuildingScores(reportId: string): Promise<any> {
    return http.get(`/analysis/reports/${reportId}/building-scores`)
  },

  /**
   * Get chart data for visualization
   */
  async getChartData(reportId: string, chartType: string): Promise<ChartData> {
    return http.get<ChartData>(`/analysis/reports/${reportId}/charts/${chartType}`)
  },

  /**
   * Export report to file
   */
  async exportReport(reportId: string, format: string): Promise<Blob> {
    const response = await http.get(`/analysis/reports/${reportId}/export`, {
      params: { format },
      responseType: 'blob'
    })
    return response
  },

  /**
   * Delete report
   */
  async deleteReport(reportId: string): Promise<void> {
    return http.delete(`/analysis/reports/${reportId}`)
  }
}

export default analysisService
