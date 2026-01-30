import { useAuthStore } from '@/store'
import { useCallback } from 'react'
import { useMutation } from '@tanstack/react-query'
import { authService } from '@/services'

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

/**
 * Hook for changing password
 */
export const useChangePassword = () => {
  return useMutation({
    mutationFn: (data: { oldPassword: string; newPassword: string }) =>
      authService.changePassword(data)
  })
}
