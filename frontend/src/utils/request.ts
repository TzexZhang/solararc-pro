import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse, AxiosError } from 'axios'
import { message } from 'antd'
import { ApiError } from '@/types'
import { API_BASE_URL, API_TIMEOUT } from '@/config'
import { useAuthStore } from '@/store'

// Create axios instance
const request: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: API_TIMEOUT,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor
request.interceptors.request.use(
  (config) => {
    // Get token from zustand authStore (via localStorage)
    const storedAuth = localStorage.getItem('auth-storage')
    if (storedAuth) {
      try {
        const authData = JSON.parse(storedAuth)
        const token = authData?.state?.token
        if (token) {
          config.headers.Authorization = `Bearer ${token}`
        }
      } catch (e) {
        console.error('Failed to parse auth storage:', e)
      }
    }
    // Fallback to old token storage for backwards compatibility
    if (!config.headers.Authorization && localStorage.getItem('token')) {
      config.headers.Authorization = `Bearer ${localStorage.getItem('token')}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
request.interceptors.response.use(
  (response: AxiosResponse) => {
    // Extract data field from API response if it exists
    const { data } = response.data
    return data !== undefined ? data : response.data
  },
  (error: AxiosError<ApiError>) => {
    if (error.response) {
      const { status, data } = error.response

      // Handle specific error codes
      switch (status) {
        case 401:
          // Unauthorized - clear auth state and redirect to login
          // Use authStore's logout method with callApi=false to avoid infinite loop
          const authStore = useAuthStore.getState()
          authStore.logout(false) // Don't call API, just clear local state
          message.error('登录已过期，请重新登录')
          // Let the auth state change trigger the redirect via ProtectedRoute
          break

        case 403:
          message.error('没有权限访问此资源')
          break

        case 404:
          message.error('请求的资源不存在')
          break

        case 500:
          message.error('服务器内部错误，请稍后重试')
          break

        default:
          // Show error message from API if available
          const errorMessage = data?.message || data?.error || '请求失败，请稍后重试'
          message.error(errorMessage)
      }

      return Promise.reject(data)
    }

    // Network error
    if (error.code === 'ECONNABORTED') {
      message.error('请求超时，请检查网络连接')
    } else {
      message.error('网络错误，请检查网络连接')
    }

    return Promise.reject(error)
  }
)

// Generic request methods
export const http = {
  get: <T = any>(url: string, config?: AxiosRequestConfig): Promise<T> => {
    return request.get(url, config)
  },

  post: <T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> => {
    return request.post(url, data, config)
  },

  put: <T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> => {
    return request.put(url, data, config)
  },

  delete: <T = any>(url: string, config?: AxiosRequestConfig): Promise<T> => {
    return request.delete(url, config)
  },

  patch: <T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> => {
    return request.patch(url, data, config)
  }
}

export default request
