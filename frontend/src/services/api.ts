/**
 * API Service entry point
 */

import { authService } from './authService'
import { buildingService } from './buildingService'
import { solarService } from './solarService'
import { shadowService } from './shadowService'
import { analysisService } from './analysisService'

export const api = {
  auth: authService,
  buildings: buildingService,
  solar: solarService,
  shadows: shadowService,
  analysis: analysisService
}

export default api
