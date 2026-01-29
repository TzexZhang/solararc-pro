import { useEffect } from 'react'
import { Card, Statistic, Row, Col, Button, Space, DatePicker, Slider } from 'antd'
import { PlayCircleOutlined, PauseCircleOutlined, SunOutlined, ClockCircleOutlined } from '@ant-design/icons'
import { useAppStore } from '@/store/useAppStore'
import { solarApi } from '@/services/api'
import dayjs from 'dayjs'

const HomePage = () => {
  const {
    viewport,
    currentHour,
    isPlaying,
    playbackSpeed,
    setViewport,
    setCurrentHour,
    setIsPlaying,
    setPlaybackSpeed,
  } = useAppStore()

  // 获取太阳位置
  const { data: solarData } = solarApi.getPosition.useQuery({
    lat: viewport.latitude,
    lng: viewport.longitude,
    date: dayjs().format('YYYY-MM-DD'),
    hour: currentHour,
    minute: 0,
  })

  return (
    <div className="home-page">
      {/* 地图区域 */}
      <div className="map-container" style={{ height: 'calc(100vh - 200px)' }}>
        <Card>
          <div
            id="map"
            style={{
              width: '100%',
              height: 'calc(100vh - 250px)',
              backgroundColor: '#f0f0f0',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}
          >
            📍 地图组件将在此处渲染
          </div>
        </Card>
      </div>

      {/* 控制面板 */}
      <div className="control-panel" style={{ marginTop: 16 }}>
        <Row gutter={16}>
          {/* 日期选择 */}
          <Col span={6}>
            <Card title="日期选择" size="small">
              <DatePicker
                style={{ width: '100%' }}
                defaultValue={dayjs()}
                format="YYYY-MM-DD"
                onChange={(date) => {
                  if (date) {
                    console.log('选择日期:', date.format('YYYY-MM-DD'))
                  }
                }}
              />
            </Card>
          </Col>

          {/* 时间控制 */}
          <Col span={10}>
            <Card title="时间控制" size="small">
              <Space direction="vertical" style={{ width: '100%' }}>
                <div>
                  <div style={{ marginBottom: 8 }}>
                    时间: {currentHour.toString().padStart(2, '0')}:00
                  </div>
                  <Slider
                    min={0}
                    max={23}
                    value={currentHour}
                    onChange={(value) => setCurrentHour(value)}
                    marks={{
                      0: '0:00',
                      6: '6:00',
                      12: '12:00',
                      18: '18:00',
                      23: '23:00',
                    }}
                  />
                </div>
                <Space>
                  <Button
                    type={isPlaying ? 'default' : 'primary'}
                    icon={isPlaying ? <PauseCircleOutlined /> : <PlayCircleOutlined />}
                    onClick={() => setIsPlaying(!isPlaying)}
                  >
                    {isPlaying ? '暂停' : '播放'}
                  </Button>
                  <Button onClick={() => setCurrentHour(6)}>日出</Button>
                  <Button onClick={() => setCurrentHour(12)}>正午</Button>
                  <Button onClick={() => setCurrentHour(18)}>日落</Button>
                </Space>
              </Space>
            </Card>
          </Col>

          {/* 太阳参数 */}
          <Col span={8}>
            <Card title="太阳参数" size="small">
              <Row gutter={16}>
                <Col span={12}>
                  <Statistic
                    title="太阳高度角"
                    value={solarData?.data?.solar_altitude || 0}
                    suffix="°"
                    precision={1}
                    prefix={<SunOutlined />}
                  />
                </Col>
                <Col span={12}>
                  <Statistic
                    title="太阳方位角"
                    value={solarData?.data?.solar_azimuth || 0}
                    suffix="°"
                    precision={1}
                  />
                </Col>
              </Row>
              <Row gutter={16} style={{ marginTop: 16 }}>
                <Col span={12}>
                  <Statistic
                    title="日出时间"
                    value={solarData?.data?.sunrise_time || '--:--'}
                    prefix={<ClockCircleOutlined />}
                  />
                </Col>
                <Col span={12}>
                  <Statistic
                    title="日落时间"
                    value={solarData?.data?.sunset_time || '--:--'}
                  />
                </Col>
              </Row>
            </Card>
          </Col>
        </Row>
      </div>
    </div>
  )
}

export default HomePage
