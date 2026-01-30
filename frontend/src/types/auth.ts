import { LatLng } from './common'

export interface User {
  id: string
  email: string
  nickname?: string
  is_active: boolean
  is_locked: boolean
  last_login_at?: string
  last_login_ip?: string
  created_at: string
  updated_at: string
}

export interface LoginRequest {
  email: string
  password: string
}

export interface RegisterRequest {
  email: string
  password: string
  nickname?: string
}

export interface AuthResponse {
  access_token: string
  token_type: string
  expires_in: number
  user: User
}

export interface ChangePasswordRequest {
  old_password: string
  new_password: string
}

export interface ForgotPasswordRequest {
  email: string
}

export interface ResetPasswordRequest {
  token: string
  new_password: string
}

export interface UserProfile {
  id: string
  email: string
  nickname?: string
  created_at: string
  last_login_at?: string
}

export interface UserSettings {
  map_center?: LatLng
  map_zoom?: number
  analysis_date?: string
  current_hour?: number
  view_mode?: string
}

export interface AuthState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  isLoading: boolean
}
