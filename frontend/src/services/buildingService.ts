import { http } from '@/utils/request'
import type {
  Building,
  BuildingQueryParams,
  BuildingListResponse,
  BuildingImportParams,
  BuildingImportResult
} from '@/types'

/**
 * Building Data API
 */
export const buildingService = {
  /**
   * Get buildings in bounding box
   */
  async getBuildingsInBounds(params: BuildingQueryParams): Promise<BuildingListResponse> {
    return http.get<BuildingListResponse>('/buildings/bbox', { params })
  },

  /**
   * Get single building by ID
   */
  async getBuildingById(id: string): Promise<Building> {
    return http.get<Building>(`/buildings/${id}`)
  },

  /**
   * Import building data from file
   */
  async importBuildings(params: BuildingImportParams): Promise<BuildingImportResult> {
    const formData = new FormData()
    formData.append('file', params.file)
    if (params.city) {
      formData.append('city', params.city)
    }

    return http.post<BuildingImportResult>('/buildings/import', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },

  /**
   * Create new building
   */
  async createBuilding(data: Partial<Building>): Promise<Building> {
    return http.post<Building>('/buildings', data)
  },

  /**
   * Update building
   */
  async updateBuilding(id: string, data: Partial<Building>): Promise<Building> {
    return http.put<Building>(`/buildings/${id}`, data)
  },

  /**
   * Delete building
   */
  async deleteBuilding(id: string): Promise<void> {
    return http.delete(`/buildings/${id}`)
  },

  /**
   * Batch delete buildings
   */
  async batchDeleteBuildings(ids: string[]): Promise<void> {
    return http.post('/buildings/batch-delete', { ids })
  }
}

export default buildingService
