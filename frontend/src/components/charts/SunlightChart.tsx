import React, { useMemo } from 'react'
import ReactECharts from 'echarts-for-react'
import { useMapStore } from '@/store'
import { useDailySolarPositions } from '@/hooks'
import './SunlightChart.css'

export const SunlightChart: React.FC = () => {
  const { currentDate, viewport } = useMapStore()
  const { data: dailyPositions, isLoading } = useDailySolarPositions(currentDate)

  const chartOption = useMemo(() => {
    if (!dailyPositions) return {}

    const hours = dailyPositions.positions.map((p) => p.hour)
    const altitudes = dailyPositions.positions.map((p) => p.altitude)
    const azimuths = dailyPositions.positions.map((p) => p.azimuth)

    return {
      title: {
        text: `太阳轨迹 - ${currentDate}`,
        left: 'center',
        textStyle: {
          fontSize: 16,
          fontWeight: 600
        }
      },
      tooltip: {
        trigger: 'axis',
        formatter: (params: any) => {
          const hour = params[0].name
          const altitude = params[0].value
          const azimuth = params[1].value
          return `时间: ${String(hour).padStart(2, '0')}:00<br/>高度角: ${altitude.toFixed(1)}°<br/>方位角: ${azimuth.toFixed(1)}°`
        }
      },
      legend: {
        data: ['高度角', '方位角'],
        bottom: 10
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '15%',
        top: '15%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        data: hours,
        name: '时间 (小时)',
        axisLabel: {
          formatter: (value: number) => `${String(value).padStart(2, '0')}:00`
        }
      },
      yAxis: [
        {
          type: 'value',
          name: '高度角 (°)',
          position: 'left',
          min: -90,
          max: 90
        },
        {
          type: 'value',
          name: '方位角 (°)',
          position: 'right',
          min: 0,
          max: 360
        }
      ],
      series: [
        {
          name: '高度角',
          type: 'line',
          data: altitudes,
          smooth: true,
          itemStyle: {
            color: '#ff7f50'
          },
          areaStyle: {
            color: {
              type: 'linear',
              x: 0,
              y: 0,
              x2: 0,
              y2: 1,
              colorStops: [
                { offset: 0, color: 'rgba(255, 127, 80, 0.3)' },
                { offset: 1, color: 'rgba(255, 127, 80, 0.05)' }
              ]
            }
          }
        },
        {
          name: '方位角',
          type: 'line',
          yAxisIndex: 1,
          data: azimuths,
          smooth: true,
          itemStyle: {
            color: '#1890ff'
          }
        }
      ]
    }
  }, [dailyPositions, currentDate])

  if (isLoading) {
    return <div className="chart-loading">加载中...</div>
  }

  return (
    <div className="sunlight-chart-container">
      <ReactECharts option={chartOption} style={{ height: '400px' }} />
    </div>
  )
}

export default SunlightChart
