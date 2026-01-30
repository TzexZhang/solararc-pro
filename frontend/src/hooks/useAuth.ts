import { useAuthStore } from '@/store'
import { useCallback } from 'react'

export const useAuth = () => {
  const {
    user,
    token,
    isAuthenticated,
    isLoading,
    login,
    register,
    logout,
    getCurrentUser,
    updateUser,
    setLoading
  } = useAuthStore()

  // Check if user has specific role
  const hasRole = useCallback((role: string) => {
    // Implement role checking logic here
    return true
  }, [])

  // Check if user has permission
  const hasPermission = useCallback((permission: string) => {
    // Implement permission checking logic here
    return true
  }, [])

  return {
    user,
    token,
    isAuthenticated,
    isLoading,
    login,
    register,
    logout,
    getCurrentUser,
    updateUser,
    setLoading,
    hasRole,
    hasPermission
  }
}

export default useAuth
