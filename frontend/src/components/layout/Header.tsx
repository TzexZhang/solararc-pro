import React from 'react'
import { Layout, Dropdown, Avatar, Space, Button, Tooltip } from 'antd'
import { Outlet, useNavigate, useLocation } from 'react-router-dom'
import {
  UserOutlined,
  LogoutOutlined,
  MenuFoldOutlined,
  MenuUnfoldOutlined,
  SettingOutlined,
  SunOutlined,
  MoonOutlined
} from '@ant-design/icons'
import { useAuth } from '@/hooks'
import { useMapStore, useAppStore } from '@/store'
import './Header.css'

const { Header: AntHeader } = Layout

export const Header: React.FC = () => {
  const navigate = useNavigate()
  const location = useLocation()
  const { user, logout, isAuthenticated } = useAuth()
  const { sidebarCollapsed, setSidebarCollapsed } = useMapStore()
  const { theme, toggleTheme } = useAppStore()

  const handleLogout = async () => {
    await logout()
    navigate('/login')
  }

  const menuItems = [
    {
      key: 'profile',
      icon: <UserOutlined />,
      label: '个人资料',
      onClick: () => navigate('/settings')
    },
    {
      key: 'settings',
      icon: <SettingOutlined />,
      label: '设置',
      onClick: () => navigate('/settings')
    },
    {
      type: 'divider' as const
    },
    {
      key: 'logout',
      icon: <LogoutOutlined />,
      label: '退出登录',
      onClick: handleLogout
    }
  ]

  return (
    <AntHeader className="layout-header">
      <div className="header-left">
        <Button
          type="text"
          icon={sidebarCollapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />}
          onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
          className="sidebar-toggle"
        />
        <div className="logo">SolarArc Pro</div>
      </div>

      <div className="header-right">
        {/* 主题切换按钮 */}
        <Tooltip title={theme === 'light' ? '切换到深色模式' : '切换到浅色模式'}>
          <Button
            type="text"
            icon={theme === 'light' ? <MoonOutlined /> : <SunOutlined />}
            onClick={toggleTheme}
            className="theme-toggle"
          />
        </Tooltip>

        {isAuthenticated && user ? (
          <Dropdown menu={{ items: menuItems }} placement="bottomRight">
            <Space className="user-info" style={{ cursor: 'pointer' }}>
              <Avatar size="small" icon={<UserOutlined />} />
              <span className="user-name">{user.nickname || user.email}</span>
            </Space>
          </Dropdown>
        ) : (
          <Space>
            <Button type="link" onClick={() => navigate('/login')}>
              登录
            </Button>
            <Button type="primary" onClick={() => navigate('/register')}>
              注册
            </Button>
          </Space>
        )}
      </div>
    </AntHeader>
  )
}

export default Header
