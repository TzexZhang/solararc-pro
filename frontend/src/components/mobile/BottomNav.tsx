import React from 'react'
import { TabBar } from 'antd-mobile'
import {
  HomeOutlined,
  DashboardOutlined,
  FileTextOutlined,
  UserOutlined
} from '@ant-design/icons'
import { useNavigate, useLocation } from 'react-router-dom'
import './BottomNav.css'

export const BottomNav: React.FC = () => {
  const navigate = useNavigate()
  const location = useLocation()

  const tabs = [
    {
      key: '/',
      title: '首页',
      icon: <HomeOutlined />
    },
    {
      key: '/dashboard',
      title: '仪表盘',
      icon: <DashboardOutlined />
    },
    {
      key: '/reports',
      title: '报告',
      icon: <FileTextOutlined />
    },
    {
      key: '/profile',
      title: '我的',
      icon: <UserOutlined />
    }
  ]

  const handleChange = (key: string) => {
    navigate(key)
  }

  return (
    <div className="bottom-nav-container">
      <TabBar activeKey={location.pathname} onChange={handleChange}>
        {tabs.map((tab) => (
          <TabBar.Item key={tab.key} icon={tab.icon} title={tab.title} />
        ))}
      </TabBar>
    </div>
  )
}

export default BottomNav
