import React, { useState } from 'react'
import { Layout, Card, Form, Select, DatePicker, Button, Space, Spin, Alert } from 'antd'
import { Header, Sidebar, Footer } from '@/components/layout'
import { useMapStore } from '@/store'
import { useNavigate } from 'react-router-dom'
import dayjs from 'dayjs'
import './AnalysisPage.css'

const { Content } = Layout
const { RangePicker } = DatePicker

export const AnalysisPage: React.FC = () => {
  const navigate = useNavigate()
  const { sidebarCollapsed, viewport } = useMapStore()
  const [loading, setLoading] = useState(false)
  const [analysisType, setAnalysisType] = useState<'daily' | 'seasonal' | 'custom'>('daily')
  const [dateRange, setDateRange] = useState<any>([dayjs(), dayjs()])

  const handleStartAnalysis = async () => {
    setLoading(true)
    // TODO: Implement analysis logic
    setTimeout(() => {
      setLoading(false)
      navigate('/reports')
    }, 2000)
  }

  return (
    <Layout className="analysis-page">
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
            <div className="analysis-content">
              <div className="page-header">
                <h1 className="page-title">日照分析</h1>
                <Button onClick={() => navigate('/')}>返回首页</Button>
              </div>

              <Card className="analysis-config-card">
                <Form layout="vertical" onFinish={handleStartAnalysis}>
                  <Form.Item label="分析类型">
                    <Select
                      value={analysisType}
                      onChange={setAnalysisType}
                      options={[
                        { value: 'daily', label: '日分析' },
                        { value: 'seasonal', label: '季节分析' },
                        { value: 'custom', label: '自定义分析' }
                      ]}
                    />
                  </Form.Item>

                  <Form.Item label="分析位置">
                    <Space direction="vertical" style={{ width: '100%' }}>
                      <div>纬度: {viewport.latitude.toFixed(4)}</div>
                      <div>经度: {viewport.longitude.toFixed(4)}</div>
                    </Space>
                  </Form.Item>

                  <Form.Item label="分析日期范围">
                    <RangePicker
                      value={dateRange}
                      onChange={setDateRange}
                      style={{ width: '100%' }}
                    />
                  </Form.Item>

                  <Form.Item>
                    <Button type="primary" htmlType="submit" loading={loading} size="large">
                      开始分析
                    </Button>
                  </Form.Item>
                </Form>
              </Card>

              <Card className="analysis-info-card">
                <Alert
                  message="分析说明"
                  description="选择分析类型和日期范围后，点击开始分析按钮进行日照分析。分析完成后将生成详细的日照报告。"
                  type="info"
                  showIcon
                />
              </Card>
            </div>
          </Content>
          <Footer />
        </Layout>
      </Layout>
    </Layout>
  )
}

export default AnalysisPage
