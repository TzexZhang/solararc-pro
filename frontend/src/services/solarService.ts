import { http } from '@/utils/request'
import type {
  SolarPosition,
  SolarPositionParams,
  DailySolarPosition
} from '@/types'

/**
 * Solar Position Calculation API
 */
export const solarService = {
  /**
   * Calculate solar position for specific time and location
   */
  async getSolarPosition(params: SolarPositionParams): Promise<SolarPosition> {
    return http.get<SolarPosition>('/solar/position', { params })
  },

  /**
   * Get daily solar positions (24 hours)
   */
  async getDailySolarPositions(
    lat: number,
    lng: number,
    date?: string
  ): Promise<DailySolarPosition> {
    const params: any = { lat, lng }
    if (date) {
      params.date = date
    }
    return http.get<DailySolarPosition>('/solar/daily-positions', { params })
  },

  /**
   * Get sunrise and sunset times
   */
  async getSunriseSunset(lat: number, lng: number, date?: string): Promise<{
    sunrise: string
    sunset: string
    day_length: number
  }> {
    const params: any = { lat, lng }
    if (date) {
      params.date = date
    }
    return http.get('/solar/sunrise-sunset', { params })
  }
}

export default solarService
