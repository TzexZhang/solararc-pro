import { ViewMode, LatLng, Bounds } from './common'

export interface MapViewState {
  latitude: number
  longitude: number
  zoom: number
  pitch?: number
  bearing?: number
}

export interface MapState {
  viewport: MapViewState
  viewMode: ViewMode
  isLoading: boolean
  selectedBuilding: string | null
  showShadows: boolean
  showBuildings: boolean
}

export interface MapLayerConfig {
  id: string
  type: string
  visible: boolean
  opacity: number
  minZoom?: number
  maxZoom?: number
}

export interface TimelineState {
  currentHour: number // 0-23
  isPlaying: boolean
  playbackSpeed: number // 1, 2, 5, 10
  date: string
}

export interface MapStyle {
  id: string
  name: string
  url: string
  thumbnail?: string
}

export interface BuildingLayerData {
  id: string
  type: 'Feature'
  properties: {
    name?: string
    height: number
    building_type: string
  }
  geometry: {
    type: 'Polygon'
    coordinates: number[][][]
  }
}

export interface ShadowLayerData {
  id: string
  type: 'Feature'
  properties: {
    building_id: string
    area: number
  }
  geometry: {
    type: 'Polygon'
    coordinates: number[][][]
  }
}
