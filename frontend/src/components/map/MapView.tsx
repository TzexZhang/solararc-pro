import React, { useRef, useEffect, useState } from 'react'
import mapboxgl from 'mapbox-gl'
import { Map, MapRef, NavigationControl, FullscreenControl, ScaleControl } from 'react-map-gl'
import { Button, DatePicker, Space, Select } from 'antd'
import { ClockCircleOutlined, SunOutlined, PlayCircleOutlined, PauseCircleOutlined } from '@ant-design/icons'
import dayjs from 'dayjs'
import { useMapStore } from '@/store'
import { MAPBOX_ACCESS_TOKEN } from '@/config'
import type { Building } from '@/types'
import { LocationSearch } from './LocationSearch'
import './MapView.css'

const { RangePicker } = DatePicker

// Mapbox access token
mapboxgl.accessToken = MAPBOX_ACCESS_TOKEN

// 计算太阳位置（基于日期和时间）
const calculateSunPosition = (date: Date, hour: number, lat: number = 39.9042) => {
  const dayOfYear = Math.floor((date.getTime() - new Date(date.getFullYear(), 0, 0).getTime()) / 86400000)

  // 太阳赤纬角（简化公式）
  const declination = 23.45 * Math.sin((360 / 365) * (dayOfYear + 284) * Math.PI / 180)

  // 时角（正午为0，每小时15度）
  const hourAngle = (hour - 12) * 15

  // 太阳高度角和方位角
  const latRad = lat * Math.PI / 180
  const decRad = declination * Math.PI / 180
  const haRad = hourAngle * Math.PI / 180

  const elevation = Math.asin(
    Math.sin(latRad) * Math.sin(decRad) +
    Math.cos(latRad) * Math.cos(decRad) * Math.cos(haRad)
  ) * 180 / Math.PI

  const azimuth = Math.atan2(
    Math.sin(haRad),
    Math.cos(haRad) * Math.sin(latRad) - Math.tan(decRad) * Math.cos(latRad)
  ) * 180 / Math.PI + 180

  return { elevation, azimuth }
}

// 计算建筑阴影多边形
const calculateShadowPolygon = (building: any, sunPos: { elevation: number, azimuth: number }) => {
  const { elevation, azimuth } = sunPos
  const height = building.total_height || 50

  if (elevation < 5) return null

  const shadowLength = height / Math.tan(elevation * Math.PI / 180)
  const shadowDirection = (azimuth + 180) % 360

  const coordinates = building.footprint?.coordinates?.[0] || building.footprint?.coordinates
  if (!coordinates || coordinates.length < 3) return null

  const shadowCoords = coordinates.map((coord: number[]) => {
    const [lng, lat] = coord
    const dx = shadowLength * Math.sin(shadowDirection * Math.PI / 180) / 111000
    const dy = shadowLength * Math.cos(shadowDirection * Math.PI / 180) / 111000
    return [lng + dx, lat - dy]
  })

  return [coordinates, shadowCoords.reverse()]
}

export const MapView: React.FC = () => {
  const mapRef = useRef<MapRef>(null)
  const {
    viewport,
    setViewport,
    buildings,
    showBuildings,
    showShadows,
    currentHour,
    currentDate,
    setCurrentHour,
    setCurrentDate,
    isPlaying,
    flyToTarget,
    setFlyToTarget
  } = useMapStore()

  const [mapStyle, setMapStyle] = useState('mapbox://styles/mapbox/streets-v12')
  const [mapLoaded, setMapLoaded] = useState(false)
  const [ctrlPressed, setCtrlPressed] = useState(false)
  const [useRealTime, setUseRealTime] = useState(true)
  const [realTimeHour, setRealTimeHour] = useState(new Date().getHours())
  const [displayHour, setDisplayHour] = useState(currentHour)

  useEffect(() => {
    const { viewMode } = useMapStore.getState()
    switch (viewMode) {
      case 'map':
        setMapStyle('mapbox://styles/mapbox/standard')
        break
      case 'white-model':
        setMapStyle('mapbox://styles/mapbox/standard')
        break
      case 'hybrid':
        setMapStyle('mapbox://styles/mapbox/standard-satellite')
        break
    }
  }, [useMapStore.getState().viewMode])

  // 设置中文语言和启用Mapbox真实3D建筑、地形、水面效果
  useEffect(() => {
    if (!mapRef.current || !mapLoaded) return
    const map = mapRef.current.getMap()

    // 添加真实地形数据（最新的Mapbox Terrain DEM v1）
    if (!map.getSource('mapbox-dem')) {
      map.addSource('mapbox-dem', {
        type: 'raster-dem',
        url: 'mapbox://mapbox.mapbox-terrain-dem-v1',
        tileSize: 512,
        maxzoom: 18
      })

      // 设置地形夸张度，增强3D效果
      map.setTerrain({ source: 'mapbox-dem', exaggeration: 1.5 })
    }

    // 设置大气效果和雾气
    map.setFog({
      'horizon-blend': 0.1,
      'color': '#ffffff',
      'high-color': '#add8e6',
      'space-color': '#d8f2ff',
      'star-intensity': 0.15
    })

    // 设置天空层
    map.setSky({
      'sky-gradient': [
        'interpolate',
        ['linear'],
        ['sky-angle'],
        0,
        'rgba(135, 206, 235, 1)', // 天蓝色
        0.5,
        'rgba(255, 255, 255, 1)', // 白色
        1,
        'rgba(255, 255, 255, 1)'
      ],
      'sky-gradient-center': [0, 0],
      'sky-gradient-radius': '90deg',
      'atmosphere-blend': ['interpolate', ['linear'], ['zoom'], 0, 1, 12, 0]
    })

    // 配置Mapbox中文标签 - 支持Mapbox Standard风格
    map.getStyle().layers.forEach((layer: any) => {
      if (layer.type === 'symbol' && layer.layout?.['text-field']) {
        // 设置中文优先的文本字段 - Mapbox Standard使用不同的属性名
        map.setLayoutProperty(layer.id, 'text-field', ['coalesce',
          ['get', 'name_zh-Hans'],        // 简体中文（Mapbox Standard）
          ['get', 'name_zh-Hant'],        // 繁体中文
          ['get', 'name_zh'],             // 备用中文
          ['get', 'name:zh'],             // OSM标准中文
          ['get', 'name'],
          ['get', 'name_en']             // 英文备用
        ])

        // 设置支持中文的字体栈
        try {
          map.setLayoutProperty(layer.id, 'text-font', [
            'Noto Sans Regular',
            'Noto Sans Bold',
            'Arial Unicode MS Regular',
            'Microsoft YaHei Regular',
            'SimHei Regular',
            'sans-serif'
          ])
        } catch (err) {
          console.warn(`Failed to set font for layer ${layer.id}:`, err)
        }
      }
    })

    // 启用Mapbox 3D建筑图层（真实建筑数据）- Standard风格自带3D建筑
    // 只需要调整样式属性
    const buildingLayers = map.getStyle().layers
      .filter((layer: any) =>
        layer.id.includes('building') ||
        layer.id.includes('3d') ||
        (layer.type === 'fill-extrusion')
      )

    buildingLayers.forEach((layer: any) => {
      try {
        map.setPaintProperty(layer.id, 'fill-extrusion-color', [
          'interpolate', ['linear'],
          ['get', 'height'],
          0, 'hsl(210, 80%, 96%)',          // 低楼层：浅蓝白色
          50, 'hsl(210, 65%, 85%)',          // 中楼层：中等蓝色
          100, 'hsl(210, 50%, 70%)',         // 高楼层：深蓝色
          200, 'hsl(210, 35%, 55%)',         // 超高层：深蓝紫色
          400, 'hsl(210, 20%, 40%)'           // 摩天大楼：深紫色
        ])
        map.setPaintProperty(layer.id, 'fill-extrusion-height', ['coalesce', ['get', 'height'], 5])
        map.setPaintProperty(layer.id, 'fill-extrusion-base', ['coalesce', ['get', 'min_height'], 0])
        map.setPaintProperty(layer.id, 'fill-extrusion-opacity', 0.9)
        map.setPaintProperty(layer.id, 'fill-extrusion-vertical-gradient', true)
        map.setPaintProperty(layer.id, 'fill-extrusion-vertical-gradient', true)
      } catch {}
    })

    // 优化水系图层 - 添加真实水面效果
    const waterLayers = map.getStyle().layers.filter((layer: any) =>
      layer.id.includes('water') || layer.type === 'fill' && layer.id.includes('water')
    )

    waterLayers.forEach((layer: any) => {
      try {
        if (layer.type === 'fill' && layer.id.includes('water')) {
          // 设置水面颜色和透明度
          map.setPaintProperty(layer.id, 'fill-color', '#4FA9E0')
          map.setPaintProperty(layer.id, 'fill-opacity', 0.7)
        }
        if (layer.type === 'symbol' && layer.id.includes('label')) {
          map.setLayoutProperty(layer.id, 'text-field', ['coalesce',
            ['get', 'name_zh'],
            ['get', 'name:zh'],
            ['get', 'name']
          ])
        }
      } catch {}
    })

    // 优化道路图层
    const roadLayers = map.getStyle().layers.filter((layer: any) =>
      layer.id.includes('road') || layer.id.includes('street') || layer.id.includes('highway')
    )

    roadLayers.forEach((layer: any) => {
      try {
        if (layer.paint?.['road-opacity'] !== undefined) {
          map.setPaintProperty(layer.id, 'road-opacity', 0.8)
        }
      } catch {}
    })

    // 优化公园绿地
    const parkLayers = map.getStyle().layers.filter((layer: any) =>
      layer.id.includes('park') || layer.id.includes('green') || layer.id.includes('landcover')
    )

    parkLayers.forEach((layer: any) => {
      try {
        if (layer.paint?.['fill-color'] !== undefined) {
          map.setPaintProperty(layer.id, 'fill-color', '#7CD47C')
        }
      } catch {}
    })

  }, [mapLoaded])

  // 监听Ctrl键状态
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Control') setCtrlPressed(true)
    }
    const handleKeyUp = (e: KeyboardEvent) => {
      if (e.key === 'Control') setCtrlPressed(false)
    }

    window.addEventListener('keydown', handleKeyDown)
    window.addEventListener('keyup', handleKeyUp)
    return () => {
      window.removeEventListener('keydown', handleKeyDown)
      window.removeEventListener('keyup', handleKeyUp)
    }
  }, [])

  // 实时时间更新
  useEffect(() => {
    if (!useRealTime) return

    const updateRealTime = () => {
      const now = new Date()
      const hour = now.getHours()
      setRealTimeHour(hour)
      setCurrentHour(hour)
      setCurrentDate(now.toISOString().split('T')[0])
    }

    updateRealTime()
    const interval = setInterval(updateRealTime, 60000)
    return () => clearInterval(interval)
  }, [useRealTime, setCurrentHour, setCurrentDate])

  // Add 3D building layer when map loads
  useEffect(() => {
    if (!mapRef.current || !mapLoaded || !showBuildings || buildings.length === 0) return
    const map = mapRef.current.getMap()

    if (map.getLayer('buildings-3d')) {
      map.removeLayer('buildings-3d')
      map.removeSource('buildings-source')
    }

    map.addSource('buildings-source', {
      type: 'geojson',
      data: {
        type: 'FeatureCollection',
        features: buildings.map((building: Building) => ({
          type: 'Feature',
          properties: {
            height: building.total_height || 50,
            name: building.name || 'Unknown',
            color: '#1890ff'
          },
          geometry: building.footprint
        }))
      }
    })

    map.addLayer({
      id: 'buildings-3d',
      type: 'fill-extrusion',
      source: 'buildings-source',
      paint: {
        'fill-extrusion-color': ['get', 'color', ['get', 'height']],
        'fill-extrusion-height': ['get', 'height'],
        'fill-extrusion-base': 0,
        'fill-extrusion-opacity': 0.8,
        'fill-extrusion-vertical-gradient': true
      }
    }, 'building')
  }, [mapLoaded, showBuildings, buildings])

  // 添加阴影层
  useEffect(() => {
    if (!mapRef.current || !mapLoaded || !showShadows || buildings.length === 0) return
    const map = mapRef.current.getMap()

    if (map.getLayer('building-shadows')) {
      map.removeLayer('building-shadows')
      map.removeSource('shadows-source')
    }

    const date = currentDate ? new Date(currentDate) : new Date()
    const hour = useRealTime ? realTimeHour : currentHour
    const sunPos = calculateSunPosition(date, hour)

    const shadowFeatures = buildings
      .map((building: Building) => {
        const shadowCoords = calculateShadowPolygon(building, sunPos)
        if (!shadowCoords) return null
        return {
          type: 'Feature',
          properties: { name: building.name || 'Unknown' },
          geometry: { type: 'Polygon', coordinates: shadowCoords }
        }
      })
      .filter(Boolean)

    map.addSource('shadows-source', {
      type: 'geojson',
      data: { type: 'FeatureCollection', features: shadowFeatures as any }
    })

    map.addLayer({
      id: 'building-shadows',
      type: 'fill',
      source: 'shadows-source',
      paint: {
        'fill-color': '#000000',
        'fill-opacity': 0.3
      }
    })
  }, [mapLoaded, showShadows, buildings, currentHour, currentDate, realTimeHour, useRealTime])

  // 飞行动效 - 监听flyToTarget并执行飞行
  useEffect(() => {
    if (!mapRef.current || !mapLoaded || !flyToTarget) {
      console.log('[MapView] flyTo跳转跳过:', { hasMapRef: !!mapRef.current, mapLoaded, hasTarget: !!flyToTarget })
      return
    }

    console.log('[MapView] 开始flyTo跳转:', flyToTarget)

    const map = mapRef.current.getMap()

    // 使用mapboxgl的flyTo方法实现平滑飞行
    map.flyTo({
      center: [flyToTarget.longitude, flyToTarget.latitude],
      zoom: flyToTarget.zoom,
      bearing: 0,
      pitch: 60,
      speed: 1.2,
      curve: 1.42,
      essential: true
    })

    // 监听动画结束事件来清除目标
    const onFlyEnd = () => {
      console.log('[MapView] flyTo跳转完成')
      setFlyToTarget(null)
      map.off('moveend', onFlyEnd)
    }

    map.on('moveend', onFlyEnd)

    // 立即更新viewport状态
    setViewport({
      latitude: flyToTarget.latitude,
      longitude: flyToTarget.longitude,
      zoom: flyToTarget.zoom
    })

    // 清理函数
    return () => {
      map.off('moveend', onFlyEnd)
    }
  }, [flyToTarget, mapLoaded, setFlyToTarget, setViewport])

  // 同步displayHour
  useEffect(() => {
    setDisplayHour(useRealTime ? realTimeHour : currentHour)
  }, [useRealTime, realTimeHour, currentHour])

  const handleMove = (evt: any) => {
    const { viewState: { latitude, longitude, zoom, pitch, bearing } } = evt
    setViewport({ latitude, longitude, zoom, pitch, bearing })
  }

  const handleMapLoad = () => {
    setMapLoaded(true)
  }

  // 日期范围处理
  const disabledDate = (current: any) => {
    return current && (current < dayjs().subtract(7, 'days') || current > dayjs())
  }

  const handleDateChange = (dates: any) => {
    if (dates && dates[0]) {
      setCurrentDate(dates[0].format('YYYY-MM-DD'))
      setUseRealTime(false)
    }
  }

  const handleHourChange = (hour: number) => {
    setCurrentHour(hour)
    setUseRealTime(false)
  }

  const handleToggleRealTime = () => {
    setUseRealTime(!useRealTime)
  }

  // 生成小时选项
  const hourOptions = Array.from({ length: 24 }, (_, i) => ({
    label: `${String(i).padStart(2, '0')}:00`,
    value: i
  }))

  return (
    <div className="map-view-container">
      {/* 地点搜索 */}
      <LocationSearch />

      {/* 时间控制面板 */}
      <div className="time-control-panel">
        <div className="time-control-card">
          <div className="control-header">
            <SunOutlined />
            <span>阴影控制</span>
          </div>

          <div className="control-section">
            <div className="section-label">时间模式</div>
            <Space direction="vertical" style={{ width: '100%' }}>
              <Button
                type={useRealTime ? 'primary' : 'default'}
                icon={<ClockCircleOutlined />}
                onClick={handleToggleRealTime}
                block
              >
                {useRealTime ? `实时时间 (${String(displayHour).padStart(2, '0')}:00)` : '切换到实时'}
              </Button>

              {!useRealTime && (
                <>
                  <RangePicker
                    placeholder={['选择日期', '']}
                    disabledDate={disabledDate}
                    onChange={handleDateChange}
                    style={{ width: '100%' }}
                  />

                  <Select
                    value={currentHour}
                    onChange={handleHourChange}
                    options={hourOptions}
                    style={{ width: '100%' }}
                    placeholder="选择时间"
                  />
                </>
              )}
            </Space>
          </div>
        </div>
      </div>

      <Map
        ref={mapRef as any}
        {...viewport}
        onMove={handleMove}
        onMapLoad={handleMapLoad}
        mapStyle={mapStyle}
        style={{ width: '100%', height: '100%' }}
        projection="globe"
        antialias
        pitch={[viewport.pitch || 60]}
        bearing={[viewport.bearing || 0]}
        dragRotate={ctrlPressed}
        touchZoomRotate={true}
      >
        <NavigationControl position="top-right" />
        <FullscreenControl position="top-right" />
        <ScaleControl maxWidth={100} unit="metric" position="bottom-left" />
      </Map>

      {ctrlPressed && (
        <div className="rotate-hint">按住鼠标左键拖动以旋转地图</div>
      )}

      <div className="map-info-overlay">
        <div className="map-info-card">
          <div className="info-item">
            <span className="info-label">建筑数量:</span>
            <span className="info-value">{buildings.length}</span>
          </div>
          <div className="info-item">
            <span className="info-label">当前时间:</span>
            <span className="info-value">{String(displayHour).padStart(2, '0')}:00</span>
          </div>
          <div className="info-item">
            <span className="info-label">显示阴影:</span>
            <span className="info-value">{showShadows ? '是' : '否'}</span>
          </div>
          <div className="info-item">
            <span className="info-label">模式:</span>
            <span className="info-value">{useRealTime ? '实时' : '手动'}</span>
          </div>
        </div>
      </div>
    </div>
  )
}

export default MapView
