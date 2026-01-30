import React from 'react'
import { Card, Descriptions, Tag, Button, Space } from 'antd'
import { CloseOutlined, InfoCircleOutlined } from '@ant-design/icons'
import { useMapStore } from '@/store'
import { formatArea, scoreToGrade } from '@/utils/format'
import type { Building } from '@/types'
import './BuildingCard.css'

export const BuildingCard: React.FC<{ building: Building }> = ({ building }) => {
  const { setSelectedBuildingId } = useMapStore()

  const handleClose = () => {
    setSelectedBuildingId(null)
  }

  const getBuildingTypeColor = (type: string) => {
    const colors: Record<string, string> = {
      residential: 'green',
      commercial: 'blue',
      industrial: 'orange',
      public: 'purple'
    }
    return colors[type] || 'default'
  }

  const getBuildingTypeLabel = (type: string) => {
    const labels: Record<string, string> = {
      residential: '住宅',
      commercial: '商业',
      industrial: '工业',
      public: '公共设施'
    }
    return labels[type] || type
  }

  return (
    <div className="building-card">
      <Card
        title={building.name || '未命名建筑'}
        extra={
          <Button
            type="text"
            icon={<CloseOutlined />}
            onClick={handleClose}
            size="small"
          />
        }
        className="building-info-card"
      >
        <Descriptions column={1} size="small">
          <Descriptions.Item label="建筑类型">
            <Tag color={getBuildingTypeColor(building.building_type)}>
              {getBuildingTypeLabel(building.building_type)}
            </Tag>
          </Descriptions.Item>

          {building.height && (
            <Descriptions.Item label="建筑高度">
              {building.height.toFixed(2)} 米
            </Descriptions.Item>
          )}

          {building.floor_area && (
            <Descriptions.Item label="楼层面积">
              {formatArea(building.floor_area)}
            </Descriptions.Item>
          )}

          {building.floor_count && (
            <Descriptions.Item label="楼层数">{building.floor_count} 层</Descriptions.Item>
          )}

          {building.reflective_rate !== undefined && (
            <Descriptions.Item label="反射率">
              {(building.reflective_rate * 100).toFixed(0)}%
            </Descriptions.Item>
          )}

          {building.address && (
            <Descriptions.Item label="地址">{building.address}</Descriptions.Item>
          )}

          {building.sunlight_stats && (
            <>
              <Descriptions.Item label="日照时长">
                {building.sunlight_stats.avg_daily_hours.toFixed(1)} 小时/天
              </Descriptions.Item>
              <Descriptions.Item label="采光率">
                {scoreToGrade(
                  building.sunlight_stats.sunlight_rate * 100
                ).label}
              </Descriptions.Item>
            </>
          )}
        </Descriptions>

        <Space className="card-actions" style={{ marginTop: 16 }}>
          <Button type="primary" size="small" icon={<InfoCircleOutlined />}>
            详细分析
          </Button>
        </Space>
      </Card>
    </div>
  )
}

export default BuildingCard
