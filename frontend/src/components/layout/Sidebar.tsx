import React from 'react'
import { Layout, Menu } from 'antd'
import { useNavigate, useLocation } from 'react-router-dom'
import {
  HomeOutlined,
  DashboardOutlined,
  FileTextOutlined,
  SettingOutlined,
  LineChartOutlined
} from '@ant-design/icons'
import { useAuth } from '@/hooks'
import './Sidebar.css'

const { Sider } = Layout

interface SidebarProps {
  collapsed: boolean
}

export const Sidebar: React.FC<SidebarProps> = ({ collapsed }) => {
  const navigate = useNavigate()
  const location = useLocation()
  const { isAuthenticated } = useAuth()

  const menuItems = [
    {
      key: '/',
      icon: <HomeOutlined />,
      label: '首页',
      onClick: () => navigate('/')
    },
    {
      key: '/dashboard',
      icon: <DashboardOutlined />,
      label: '仪表盘',
      onClick: () => navigate('/dashboard')
    },
    ...(isAuthenticated
      ? [
          {
            key: '/reports',
            icon: <FileTextOutlined />,
            label: '分析报告',
            onClick: () => navigate('/reports')
          },
          {
            key: '/analysis',
            icon: <LineChartOutlined />,
            label: '日照分析',
            onClick: () => navigate('/analysis')
          }
        ]
      : []),
    {
      key: '/settings',
      icon: <SettingOutlined />,
      label: '设置',
      onClick: () => navigate('/settings')
    }
  ]

  const getSelectedKey = () => {
    return location.pathname
  }

  return (
    <Sider
      collapsible
      collapsed={collapsed}
      trigger={null}
      className="layout-sidebar"
      width={240}
    >
      <div className="sidebar-logo">
        {!collapsed && <span>SolarArc Pro</span>}
      </div>
      <Menu
        mode="inline"
        selectedKeys={[getSelectedKey()]}
        items={menuItems}
        className="sidebar-menu"
      />
    </Sider>
  )
}

export default Sidebar
