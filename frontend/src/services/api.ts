import axios from 'axios'
import type { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1'

class ApiClient {
  private client: AxiosInstance

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    })

    // 请求拦截器
    this.client.interceptors.request.use(
      (config) => {
        console.log(`[API] ${config.method?.toUpperCase()} ${config.url}`)
        return config
      },
      (error) => {
        return Promise.reject(error)
      }
    )

    // 响应拦截器
    this.client.interceptors.response.use(
      (response: AxiosResponse) => {
        return response.data
      },
      (error) => {
        console.error('[API Error]', error.response?.data || error.message)
        return Promise.reject(error)
      }
    )
  }

  async get<T = any>(url: string, config?: AxiosRequestConfig): Promise<T> {
    return this.client.get(url, config)
  }

  async post<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    return this.client.post(url, data, config)
  }

  async put<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    return this.client.put(url, data, config)
  }

  async delete<T = any>(url: string, config?: AxiosRequestConfig): Promise<T> {
    return this.client.delete(url, config)
  }
}

export const api = new ApiClient()

// API接口定义
export const buildingApi = {
  // 获取视野内建筑
  getBuildingsInBBox: (params: {
    min_lat: number
    max_lat: number
    min_lng: number
    max_lng: number
    include_shadow?: boolean
    analysis_date?: string
    analysis_hour?: number
  }) => api.get('/buildings/', { params }),

  // 获取单个建筑
  getBuilding: (id: number) => api.get(`/buildings/${id}`),

  // 创建建筑
  createBuilding: (data: any) => api.post('/buildings/', data),

  // 更新建筑
  updateBuilding: (id: number, data: any) => api.put(`/buildings/${id}`, data),

  // 删除建筑
  deleteBuilding: (id: number) => api.delete(`/buildings/${id}`),

  // 导入建筑
  importBuildings: (file: File, city?: string) => {
    const formData = new FormData()
    formData.append('file', file)
    if (city) formData.append('city', city)
    return api.post('/buildings/import', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },
}

export const solarApi = {
  // 获取太阳位置
  getPosition: (params: {
    lat: number
    lng: number
    date?: string
    hour?: number
    minute?: number
    timezone?: string
  }) => api.get('/solar/position', { params }),

  // 获取24小时太阳位置
  getDailyPositions: (params: {
    lat: number
    lng: number
    date?: string
    timezone?: string
  }) => api.get('/solar/daily-positions', { params }),

  // 获取日出日落
  getSunriseSunset: (params: {
    lat: number
    lng: number
    date?: string
    timezone?: string
  }) => api.get('/solar/sunrise-sunset', { params }),

  // 获取关键日期太阳位置
  getKeyDatesPositions: (params: {
    lat: number
    lng: number
    year?: number
    hour?: number
  }) => api.get('/solar/key-dates', { params }),
}

export const shadowApi = {
  // 计算阴影
  calculate: (data: {
    building_ids: number[]
    date: string
    hour: number
    minute?: number
  }) => api.post('/shadows/calculate', data),

  // 对比极端阴影
  compareExtremes: (params: {
    building_id: number
    hour?: number
  }) => api.get('/shadows/compare-extremes', { params }),

  // 获取阴影动画
  getAnimation: (params: {
    building_id: number
    date: string
    start_hour?: number
    end_hour?: number
    step_minutes?: number
  }) => api.get('/shadows/animation', { params }),

  // 清空缓存
  clearCache: (building_id?: number) =>
    api.delete('/shadows/cache', { params: { building_id } }),
}

export const analysisApi = {
  // 点日照分析
  analyzePointSunlight: (data: {
    point: { lat: number; lng: number }
    date: string
    start_hour?: number
    end_hour?: number
  }) => api.post('/analysis/point-sunlight', data),

  // 阴影重叠分析
  analyzeShadowOverlap: (data: {
    target_building_id: number
    surrounding_building_ids: number[]
    date: string
    hour: number
  }) => api.post('/analysis/shadow-overlap', data),

  // 建筑日照分析
  analyzeBuildingSunlight: (building_id: number, date: string) =>
    api.get(`/analysis/building-sunlight/${building_id}`, { params: { date } }),

  // 年度日照分析
  analyzeAnnualSunlight: (building_id: number, year?: number) =>
    api.get(`/analysis/annual-sunlight/${building_id}`, { params: { year } }),

  // 标准合规检查
  checkStandardCompliance: (building_id: number, standard?: string) =>
    api.get(`/analysis/standard-compliance/${building_id}`, { params: { standard } }),
}

export const coordApi = {
  // 坐标转换
  transform: (data: {
    coords: Array<{ lng: number; lat: number }>
    from_system: string
    to_system: string
  }) => api.post('/coords/transform', data),

  // GeoJSON坐标转换
  transformGeojson: (data: {
    geojson: any
    from_system: string
    to_system: string
  }) => api.post('/coords/transform-geojson', data),

  // 获取坐标偏移
  getOffset: (lat: number, lng: number, system: string) =>
    api.get(`/coords/offset/${lat}/${lng}`, { params: { system } }),

  // 检测坐标系
  detectSystem: (lat: number, lng: number, reference_city?: string) =>
    api.get(`/coords/detect/${lat}/${lng}`, { params: { reference_city } }),

  // 列出支持的坐标系
  listSystems: () => api.get('/coords/systems'),
}
