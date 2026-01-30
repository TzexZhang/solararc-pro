import { create } from 'zustand'
import type { AnalysisReport, SolarPosition } from '@/types'

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
  incrementNotifications: () => void
  clearNotifications: () => void
}

export const useAppStore = create<AppState>((set) => ({
  isInitialized: false,
  isLoading: false,

  solarPosition: null,

  reports: [],
  currentReport: null,

  isMobile: false,
  theme: 'light',

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

  setTheme: (theme) => set({ theme }),

  incrementNotifications: () =>
    set((state) => ({ notifications: state.notifications + 1 })),

  clearNotifications: () => set({ notifications: 0 })
}))

export default useAppStore
