import React, { useEffect, useState } from 'react'
import { Layout } from 'antd'
import { Header, Sidebar, Footer } from '@/components/layout'
import { MapView, Timeline, BuildingCard } from '@/components/map'
import { Dashboard } from '@/components/charts'
import { useMapStore, useAuth } from '@/store'
import { useBuildingsInBounds } from '@/hooks'
import './HomePage.css'

const { Content } = Layout

export const HomePage: React.FC = () => {
  const { viewport, sidebarCollapsed, selectedBuildingId, buildings } = useMapStore()
  const { isAuthenticated } = useAuth()
  const [bounds, setBounds] = useState<any>(null)

  useEffect(() => {
    // Calculate initial bounds from viewport
    const latDiff = (viewport.zoom > 12 ? 0.01 : 0.05) / (2 ** (viewport.zoom - 10))
    const lngDiff = latDiff * 2

    setBounds({
      min_lat: viewport.latitude - latDiff,
      max_lat: viewport.latitude + latDiff,
      min_lng: viewport.longitude - lngDiff,
      max_lng: viewport.longitude + lngDiff
    })
  }, [viewport.latitude, viewport.longitude, viewport.zoom])

  useBuildingsInBounds(bounds, !!bounds)

  const selectedBuilding = buildings.find((b) => b.id === selectedBuildingId)

  return (
    <Layout className="home-page">
      <Header />
      <Layout>
        <Sidebar collapsed={sidebarCollapsed} />
        <Layout
          style={{
            marginLeft: sidebarCollapsed ? 80 : 240,
            transition: 'margin-left 0.2s'
          }}
        >
          <Content className="content">
            <div className="map-wrapper">
              <MapView />
              <Dashboard />
              {selectedBuilding && <BuildingCard building={selectedBuilding} />}
              <Timeline />
            </div>
          </Content>
        </Layout>
      </Layout>
    </Layout>
  )
}

export default HomePage
