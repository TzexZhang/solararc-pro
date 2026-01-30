import React, { useEffect } from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuth } from '@/hooks'
import { useAuthStore } from '@/store'
import { HomePage, LoginPage, RegisterPage, DashboardPage, ReportsPage } from '@/pages'
import { BottomNav } from '@/components/mobile'
import './App.css'

const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated, isLoading } = useAuth()
  const { getCurrentUser } = useAuthStore()

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (token && !isAuthenticated) {
      getCurrentUser().catch(() => {
        // Token is invalid, will be handled by error
      })
    }
  }, [])

  if (isLoading) {
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

        {/* Fallback */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>

      {/* Mobile bottom navigation */}
      <BottomNav />
    </div>
  )
}

export default App
