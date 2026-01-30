import { http } from '@/utils/request'
import { storage } from '@/utils/storage'
import type {
  LoginRequest,
  RegisterRequest,
  AuthResponse,
  User,
  ChangePasswordRequest,
  ForgotPasswordRequest,
  ResetPasswordRequest
} from '@/types'

/**
 * User Authentication API
 */
export const authService = {
  /**
   * Login with email and password
   */
  async login(data: LoginRequest): Promise<AuthResponse> {
    const response = await http.post<AuthResponse>('/auth/login', data)

    // Store token and user info
    if (response.access_token) {
      storage.set('token', response.access_token)
      storage.set('user', response.user)
    }

    return response
  },

  /**
   * Register new user
   */
  async register(data: RegisterRequest): Promise<{ user_id: string }> {
    return http.post('/auth/register', data)
  },

  /**
   * Get current user info
   */
  async getCurrentUser(): Promise<User> {
    return http.get<User>('/auth/me')
  },

  /**
   * Logout
   */
  async logout(): Promise<void> {
    try {
      await http.post('/auth/logout')
    } finally {
      // Clear local storage regardless of API call success
      storage.remove('token')
      storage.remove('user')
    }
  },

  /**
   * Change password
   */
  async changePassword(data: ChangePasswordRequest): Promise<void> {
    return http.put('/auth/change-password', data)
  },

  /**
   * Request password reset email
   */
  async forgotPassword(data: ForgotPasswordRequest): Promise<void> {
    return http.post('/auth/forgot-password', data)
  },

  /**
   * Reset password with token
   */
  async resetPassword(data: ResetPasswordRequest): Promise<void> {
    return http.post('/auth/reset-password', data)
  },

  /**
   * Check if user is authenticated
   */
  isAuthenticated(): boolean {
    const token = storage.get<string>('token')
    return !!token
  },

  /**
   * Get stored user info
   */
  getStoredUser(): User | null {
    return storage.get<User>('user')
  },

  /**
   * Get stored token
   */
  getToken(): string | null {
    return storage.get<string>('token')
  }
}

export default authService
