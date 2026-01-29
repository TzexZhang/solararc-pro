import { create } from 'zustand'
import { devtools, persist } from 'zustand/middleware'

export interface Building {
  id: number
  name: string
  building_type: string
  height: number
  floor_area: number
  footprint: {
    type: string
    coordinates: number[][][]
  }
  shadow?: any
}

export interface Shadow {
  building_id: number
  shadow_polygon: any
  shadow_area: number
}

export interface Viewport {
  latitude: number
  longitude: number
  zoom: number
  bearing?: number
  pitch?: number
}

export type ViewMode = 'map' | 'white-model' | 'hybrid'

interface AppState {
  // 地图视图状态
  viewport: Viewport

  // 分析参数
  analysisDate: Date
  currentHour: number
  currentMinute: number

  // 数据
  buildings: Building[]
  shadows: Shadow[]

  // UI状态
  viewMode: ViewMode
  isLoading: boolean
  isPlaying: boolean
  playbackSpeed: number

  // 选中项
  selectedBuilding: Building | null

  // Actions
  setViewport: (viewport: Partial<Viewport>) => void
  setBuildings: (buildings: Building[]) => void
  setShadows: (shadows: Shadow[]) => void
  setAnalysisDate: (date: Date) => void
  setCurrentHour: (hour: number) => void
  setCurrentMinute: (minute: number) => void
  setViewMode: (mode: ViewMode) => void
  setIsLoading: (loading: boolean) => void
  setIsPlaying: (playing: boolean) => void
  setPlaybackSpeed: (speed: number) => void
  setSelectedBuilding: (building: Building | null) => void

  // 重置
  reset: () => void
}

const initialState = {
  viewport: {
    latitude: 39.90923, // 北京
    longitude: 116.397428,
    zoom: 14,
    bearing: 0,
    pitch: 0,
  },
  analysisDate: new Date(),
  currentHour: 12,
  currentMinute: 0,
  buildings: [],
  shadows: [],
  viewMode: 'map' as ViewMode,
  isLoading: false,
  isPlaying: false,
  playbackSpeed: 1,
  selectedBuilding: null,
}

export const useAppStore = create<AppState>()(
  devtools(
    persist(
      (set) => ({
        ...initialState,

        setViewport: (newViewport) =>
          set((state) => ({
            viewport: { ...state.viewport, ...newViewport },
          })),

        setBuildings: (buildings) => set({ buildings }),

        setShadows: (shadows) => set({ shadows }),

        setAnalysisDate: (date) => set({ analysisDate: date }),

        setCurrentHour: (hour) => set({ currentHour: hour }),

        setCurrentMinute: (minute) => set({ currentMinute: minute }),

        setViewMode: (mode) => set({ viewMode: mode }),

        setIsLoading: (loading) => set({ isLoading: loading }),

        setIsPlaying: (playing) => set({ isPlaying: playing }),

        setPlaybackSpeed: (speed) => set({ playbackSpeed: speed }),

        setSelectedBuilding: (building) => set({ selectedBuilding: building }),

        reset: () => set(initialState),
      }),
      {
        name: 'solararc-pro-storage',
        partialize: (state) => ({
          viewport: state.viewport,
          viewMode: state.viewMode,
          analysisDate: state.analysisDate,
        }),
      }
    ),
    { name: 'SolarArcPro' }
  )
)
