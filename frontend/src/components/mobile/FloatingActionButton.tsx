import React from 'react'
import { FloatButton } from 'antd'
import {
  PlusOutlined,
  ExportOutlined,
  FullscreenOutlined,
  SettingOutlined
} from '@ant-design/icons'
import './FloatingActionButton.css'

export const FloatingActionButton: React.FC = () => {
  return (
    <FloatButton.Group
      trigger="click"
      type="primary"
      icon={<PlusOutlined />}
      className="fab-container"
    >
      <FloatButton
        icon={<ExportOutlined />}
        tooltip="导出数据"
      />
      <FloatButton
        icon={<FullscreenOutlined />}
        tooltip="全屏模式"
      />
      <FloatButton
        icon={<SettingOutlined />}
        tooltip="设置"
      />
    </FloatButton.Group>
  )
}

export default FloatingActionButton
