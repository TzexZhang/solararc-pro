import React from 'react'
import { Layout } from 'antd'
import './Footer.css'

const { Footer: AntFooter } = Layout

export const Footer: React.FC = () => {
  return (
    <AntFooter className="layout-footer">
      <div className="footer-content">
        <p>&copy; 2026 SolarArc Pro. All rights reserved.</p>
        <p className="footer-links">
          <a href="https://github.com/solararc-pro" target="_blank" rel="noopener noreferrer">
            GitHub
          </a>
          <span>|</span>
          <a href="/docs">文档</a>
          <span>|</span>
          <a href="/privacy">隐私政策</a>
          <span>|</span>
          <a href="/terms">服务条款</a>
        </p>
      </div>
    </AntFooter>
  )
}

export default Footer
