import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import type { MapViewState, ViewMode, Building, ShadowResult } from '@/types'
import dayjs from 'dayjs'

interface MapState {
  // Map viewport
  viewport: MapViewState

  // View settings
  viewMode: ViewMode
  showShadows: boolean
  showBuildings: boolean

  // Timeline
  currentDate: string
  currentHour: number
  isPlaying: boolean
  playbackSpeed: number

  // Data
  buildings: Building[]
  shadows: ShadowResult[]

  // Selection
  selectedBuildingId: string | null

  // UI state
  isLoading: boolean
  sidebarCollapsed: boolean

  // Actions
  setViewport: (viewport: Partial<MapViewState>) => void
  setViewMode: (mode: ViewMode) => void
  setShowShadows: (show: boolean) => void
  setShowBuildings: (show: boolean) => void
  setCurrentDate: (date: string) => void
  setCurrentHour: (hour: number) => void
  setIsPlaying: (playing: boolean) => void
  setPlaybackSpeed: (speed: number) => void
  setBuildings: (buildings: Building[]) => void
  setShadows: (shadows: ShadowResult[]) => void
  setSelectedBuildingId: (id: string | null) => void
  setIsLoading: (loading: boolean) => void
  setSidebarCollapsed: (collapsed: boolean) => void
  resetTimeline: () => void
}

export const useMapStore = create<MapState>()(
  persist(
    (set) => ({
      // Initial viewport (Beijing)
      viewport: {
        latitude: 39.9042,
        longitude: 116.4074,
        zoom: 12,
        pitch: 0,
        bearing: 0
      },

      viewMode: 'map',
      showShadows: true,
      showBuildings: true,

      // Timeline - default to today and noon
      currentDate: dayjs().format('YYYY-MM-DD'),
      currentHour: 12,
      isPlaying: false,
      playbackSpeed: 1,

      buildings: [],
      shadows: [],

      selectedBuildingId: null,
      isLoading: false,
      sidebarCollapsed: false,

      // Actions
      setViewport: (viewport) =>
        set((state) => ({
          viewport: { ...state.viewport, ...viewport }
        })),

      setViewMode: (mode) => set({ viewMode: mode }),

      setShowShadows: (show) => set({ showShadows: show }),

      setShowBuildings: (show) => set({ showBuildings: show }),

      setCurrentDate: (date) => set({ currentDate: date }),

      setCurrentHour: (hour) => set({ currentHour: hour }),

      setIsPlaying: (playing) => set({ isPlaying: playing }),

      setPlaybackSpeed: (speed) => set({ playbackSpeed: speed }),

      setBuildings: (buildings) => set({ buildings }),

      setShadows: (shadows) => set({ shadows }),

      setSelectedBuildingId: (id) => set({ selectedBuildingId: id }),

      setIsLoading: (loading) => set({ isLoading: loading }),

      setSidebarCollapsed: (collapsed) => set({ sidebarCollapsed: collapsed }),

      resetTimeline: () =>
        set({
          currentDate: dayjs().format('YYYY-MM-DD'),
          currentHour: 12,
          isPlaying: false
        })
    }),
    {
      name: 'map-storage',
      partialize: (state) => ({
        viewport: state.viewport,
        viewMode: state.viewMode,
        currentDate: state.currentDate,
        currentHour: state.currentHour,
        sidebarCollapsed: state.sidebarCollapsed
      })
    }
  )
)

export default useMapStore
