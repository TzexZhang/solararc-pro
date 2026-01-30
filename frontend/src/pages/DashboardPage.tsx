import React from 'react'
import { Layout, Card, Row, Col } from 'antd'
import { Header, Sidebar, Footer } from '@/components/layout'
import { Dashboard } from '@/components/charts'
import { SunlightChart } from '@/components/charts/SunlightChart'
import { useMapStore } from '@/store'
import './DashboardPage.css'

const { Content } = Layout

export const DashboardPage: React.FC = () => {
  const { sidebarCollapsed } = useMapStore()

  return (
    <Layout className="dashboard-page">
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
            <div className="dashboard-content">
              <h1 className="page-title">仪表盘</h1>

              <Row gutter={[16, 16]}>
                <Col span={24}>
                  <Dashboard />
                </Col>
              </Row>

              <Row gutter={[16, 16]} style={{ marginTop: 24 }}>
                <Col xs={24} lg={24}>
                  <Card title="太阳轨迹" className="chart-card">
                    <SunlightChart />
                  </Card>
                </Col>
              </Row>
            </div>
          </Content>
          <Footer />
        </Layout>
      </Layout>
    </Layout>
  )
}

export default DashboardPage
