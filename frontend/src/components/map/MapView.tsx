import React, { useRef, useEffect, useState } from 'react'
import mapboxgl from 'mapbox-gl'
import { Map, MapRef } from 'react-map-gl'
import { PolygonLayer } from 'deck.gl'
import { DeckGL } from 'deck.gl'
import { useMapStore } from '@/store'
import type { Building } from '@/types'
import './MapView.css'

// Mapbox access token (replace with your own)
mapboxgl.accessToken =
  import.meta.env.VITE_MAPBOX_TOKEN || 'pk.your-mapbox-token-here'

export const MapView: React.FC = () => {
  const mapRef = useRef<MapRef>(null)
  const { viewport, setViewport, buildings, showBuildings, showShadows } = useMapStore()
  const [mapStyle, setMapStyle] = useState('mapbox://styles/mapbox/streets-v12')

  useEffect(() => {
    // Update map style based on view mode
    const { viewMode } = useMapStore.getState()
    switch (viewMode) {
      case 'map':
        setMapStyle('mapbox://styles/mapbox/streets-v12')
        break
      case 'white-model':
        setMapStyle('mapbox://styles/mapbox/light-v11')
        break
      case 'hybrid':
        setMapStyle('mapbox://styles/mapbox/satellite-streets-v12')
        break
    }
  }, [useMapStore.getState().viewMode])

  const handleMove = (evt: any) => {
    const {
      viewState: { latitude, longitude, zoom }
    } = evt
    setViewport({ latitude, longitude, zoom })
  }

  const buildingLayer = {
    id: 'buildings',
    type: 'fill-extrusion' as const,
    paint: {
      'fill-extrusion-color': '#1890ff',
      'fill-extrusion-height': ['get', 'height'],
      'fill-extrusion-base': 0,
      'fill-extrusion-opacity': 0.8
    }
  }

  return (
    <div className="map-view-container">
      <Map
        ref={mapRef}
        {...viewport}
        onMove={handleMove}
        mapStyle={mapStyle}
        style={{ width: '100%', height: '100%' }}
        projection="globe"
      >
        {showBuildings && (
          <buildingLayer
            id="buildings"
            type="fill-extrusion"
            source={{
              type: 'geojson',
              data: {
                type: 'FeatureCollection',
                features: buildings.map((building: Building) => ({
                  type: 'Feature',
                  properties: {
                    height: building.height,
                    name: building.name
                  },
                  geometry: building.footprint
                }))
              }
            }}
            paint={{
              'fill-extrusion-color': '#1890ff',
              'fill-extrusion-height': ['get', 'height'],
              'fill-extrusion-base': 0,
              'fill-extrusion-opacity': 0.6
            }}
          />
        )}
      </Map>
    </div>
  )
}

export default MapView
