import React from 'react'
import { Card, Row, Col, Statistic, Space } from 'antd'
import {
  SunOutlined,
  CloudOutlined,
  ClockCircleOutlined,
  BulbOutlined
} from '@ant-design/icons'
import { useSolarPosition } from '@/hooks'
import { useMapStore } from '@/store'
import './Dashboard.css'

export const Dashboard: React.FC = () => {
  const { currentHour, currentDate } = useMapStore()
  const { data: solarData, isLoading } = useSolarPosition()

  if (isLoading || !solarData) {
    return <div className="dashboard-loading">加载中...</div>
  }

  const shadowLength = solarData.solar_altitude > 0
    ? Math.tan((90 - solarData.solar_altitude) * Math.PI / 180)
    : 0

  return (
    <div className="dashboard-container">
      <Row gutter={[16, 16]}>
        <Col xs={12} sm={12} md={6}>
          <Card className="dashboard-card">
            <Statistic
              title="太阳高度角"
              value={solarData.solar_altitude}
              precision={1}
              suffix="°"
              prefix={<SunOutlined />}
              valueStyle={{ color: '#ff7f50' }}
            />
          </Card>
        </Col>

        <Col xs={12} sm={12} md={6}>
          <Card className="dashboard-card">
            <Statistic
              title="太阳方位角"
              value={solarData.solar_azimuth}
              precision={1}
              suffix="°"
              prefix={<CloudOutlined />}
              valueStyle={{ color: '#1890ff' }}
            />
          </Card>
        </Col>

        <Col xs={12} sm={12} md={6}>
          <Card className="dashboard-card">
            <Statistic
              title="阴影系数"
              value={shadowLength}
              precision={2}
              prefix={<ClockCircleOutlined />}
              valueStyle={{ color: '#52c41a' }}
            />
          </Card>
        </Col>

        <Col xs={12} sm={12} md={6}>
          <Card className="dashboard-card">
            <Statistic
              title="日照时长"
              value={solarData.day_length}
              precision={2}
              suffix="小时"
              prefix={<BulbOutlined />}
              valueStyle={{ color: '#faad14' }}
            />
          </Card>
        </Col>
      </Row>

      <Card className="time-info-card" style={{ marginTop: 16 }}>
        <Space direction="vertical" size="small" style={{ width: '100%' }}>
          <div className="time-info-row">
            <span className="time-label">日期:</span>
            <span className="time-value">{currentDate}</span>
          </div>
          <div className="time-info-row">
            <span className="time-label">时间:</span>
            <span className="time-value">{String(currentHour).padStart(2, '0')}:00</span>
          </div>
          <div className="time-info-row">
            <span className="time-label">日出:</span>
            <span className="time-value">{solarData.sunrise_time}</span>
          </div>
          <div className="time-info-row">
            <span className="time-label">日落:</span>
            <span className="time-value">{solarData.sunset_time}</span>
          </div>
        </Space>
      </Card>
    </div>
  )
}

export default Dashboard
