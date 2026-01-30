import { http } from '@/utils/request'
import type {
  ShadowCalculateParams,
  ShadowCalculateResponse,
  ShadowCompareExtremes
} from '@/types'

/**
 * Shadow Calculation API
 */
export const shadowService = {
  /**
   * Calculate shadows for buildings
   */
  async calculateShadows(params: ShadowCalculateParams): Promise<ShadowCalculateResponse> {
    return http.post<ShadowCalculateResponse>('/shadows/calculate', params)
  },

  /**
   * Get shadow comparison for winter and summer solstice
   */
  async compareShadowExtremes(buildingId: string, hour: number = 12): Promise<ShadowCompareExtremes> {
    return http.get<ShadowCompareExtremes>(`/shadows/compare-extremes`, {
      params: { building_id: buildingId, hour }
    })
  },

  /**
   * Get cached shadow data
   */
  async getCachedShadow(buildingId: string, date: string, hour: number): Promise<any> {
    return http.get(`/shadows/cache`, {
      params: { building_id: buildingId, date, hour }
    })
  }
}

export default shadowService
