import React, { useEffect, useState } from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuth } from '@/hooks'
import { useAuthStore } from '@/store'
import { HomePage, LoginPage, RegisterPage, DashboardPage, ReportsPage, AnalysisPage, SettingsPage } from '@/pages'
import { BottomNav } from '@/components/mobile'
import './App.css'

const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated, isLoading } = useAuth()
  const { getCurrentUser, token } = useAuthStore()
  const [checkingAuth, setCheckingAuth] = useState(true)

  useEffect(() => {
    const checkAuth = async () => {
      const storedAuth = localStorage.getItem('auth-storage')

      // 如果没有存储的数据，直接结束检查
      if (!storedAuth) {
        setCheckingAuth(false)
        return
      }

      try {
        const authData = JSON.parse(storedAuth)
        const hasToken = authData?.state?.token || token

        // 如果有token但未认证，尝试获取用户信息
        if (hasToken && !isAuthenticated) {
          try {
            await getCurrentUser()
          } catch (error) {
            // 获取用户信息失败，清除无效数据
            console.error('获取用户信息失败:', error)
            localStorage.removeItem('auth-storage')
          }
        }
      } catch {
        // JSON解析失败，清除无效数据
        localStorage.removeItem('auth-storage')
      }

      setCheckingAuth(false)
    }

    checkAuth()
  }, []) // 只在组件挂载时执行一次

  // Show loading while checking auth or while loading user data
  if (checkingAuth || isLoading) {
    return <div className="loading-screen">加载中...</div>
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  return <>{children}</>
}

const App: React.FC = () => {
  return (
    <div className="app">
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />

        {/* Protected routes */}
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <DashboardPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/reports"
          element={
            <ProtectedRoute>
              <ReportsPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/analysis"
          element={
            <ProtectedRoute>
              <AnalysisPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/settings"
          element={
            <ProtectedRoute>
              <SettingsPage />
            </ProtectedRoute>
          }
        />

        {/* Fallback */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>

      {/* Mobile bottom navigation */}
      <BottomNav />
    </div>
  )
}

export default App
