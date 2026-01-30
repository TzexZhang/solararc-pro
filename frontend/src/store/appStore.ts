import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import type { AnalysisReport, SolarPosition } from '@/types'

// 检测系统主题偏好
const getSystemTheme = (): 'light' | 'dark' => {
  if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
    return 'dark'
  }
  return 'light'
}

interface AppState {
  // Global app state
  isInitialized: boolean
  isLoading: boolean

  // Solar position data
  solarPosition: SolarPosition | null

  // Analysis reports
  reports: AnalysisReport[]
  currentReport: AnalysisReport | null

  // UI state
  isMobile: boolean
  theme: 'light' | 'dark'

  // Notifications
  notifications: number

  // Actions
  setInitialized: (initialized: boolean) => void
  setLoading: (loading: boolean) => void
  setSolarPosition: (position: SolarPosition | null) => void
  setReports: (reports: AnalysisReport[]) => void
  addReport: (report: AnalysisReport) => void
  removeReport: (reportId: string) => void
  setCurrentReport: (report: AnalysisReport | null) => void
  setMobile: (isMobile: boolean) => void
  setTheme: (theme: 'light' | 'dark') => void
  toggleTheme: () => void
  incrementNotifications: () => void
  clearNotifications: () => void
}

export const useAppStore = create<AppState>()(
  persist(
    (set, get) => ({
      isInitialized: false,
      isLoading: false,

      solarPosition: null,

      reports: [],
      currentReport: null,

      isMobile: false,
      theme: getSystemTheme(),

      notifications: 0,

      // Actions
      setInitialized: (initialized) => set({ isInitialized: initialized }),

      setLoading: (loading) => set({ isLoading: loading }),

      setSolarPosition: (position) => set({ solarPosition: position }),

      setReports: (reports) => set({ reports }),

      addReport: (report) =>
        set((state) => ({ reports: [report, ...state.reports] })),

      removeReport: (reportId) =>
        set((state) => ({
          reports: state.reports.filter((r) => r.id !== reportId)
        })),

      setCurrentReport: (report) => set({ currentReport: report }),

      setMobile: (isMobile) => set({ isMobile }),

      setTheme: (theme) => {
        set({ theme })
        // 更新 HTML 的 data-theme 属性
        document.documentElement.setAttribute('data-theme', theme)
      },

      toggleTheme: () => {
        const currentTheme = get().theme
        const newTheme = currentTheme === 'light' ? 'dark' : 'light'
        get().setTheme(newTheme)
      },

      incrementNotifications: () =>
        set((state) => ({ notifications: state.notifications + 1 })),

      clearNotifications: () => set({ notifications: 0 })
    }),
    {
      name: 'app-storage',
      partialize: (state) => ({
        theme: state.theme,
        isMobile: state.isMobile
      })
    }
  )
)

// 初始化时应用主题
if (typeof window !== 'undefined') {
  const storedTheme = localStorage.getItem('app-storage')
  if (storedTheme) {
    try {
      const { state } = JSON.parse(storedTheme)
      if (state?.theme) {
        document.documentElement.setAttribute('data-theme', state.theme)
      }
    } catch {
      document.documentElement.setAttribute('data-theme', getSystemTheme())
    }
  } else {
    document.documentElement.setAttribute('data-theme', getSystemTheme())
  }
}

export default useAppStore
