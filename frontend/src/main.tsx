import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import { ConfigProvider, App } from 'antd'
import zhCN from 'antd/locale/zh_CN'
import AppProvider from './providers/AppProvider'
import Router from './router'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <BrowserRouter>
      <ConfigProvider locale={zhCN}>
        <AppProvider>
          <App>
            <Router />
          </App>
        </AppProvider>
      </ConfigProvider>
    </BrowserRouter>
  </React.StrictMode>,
)
