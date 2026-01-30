import React, { createContext, useContext, useEffect, ReactNode } from 'react'
import { ConfigProvider, theme as antdTheme } from 'antd'
import { useAppStore } from '@/store'

interface ThemeContextType {
  theme: 'light' | 'dark'
}

const ThemeContext = createContext<ThemeContextType>({
  theme: 'light'
})

export const ThemeProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const { theme } = useAppStore()

  // 定义主题配置
  const lightTheme = {
    algorithm: antdTheme.defaultAlgorithm,
    token: {
      colorPrimary: '#1890ff',
      colorSuccess: '#52c41a',
      colorWarning: '#faad14',
      colorError: '#ff4d4f',
      borderRadius: 8
    }
  }

  const darkTheme = {
    algorithm: antdTheme.darkAlgorithm,
    token: {
      colorPrimary: '#177ddc',
      colorSuccess: '#49aa19',
      colorWarning: '#d89614',
      colorError: '#d32029',
      borderRadius: 8
    }
  }

  // 同步data-theme属性到documentElement
  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme)
  }, [theme])

  const contextValue = {
    theme
  }

  return (
    <ThemeContext.Provider value={contextValue}>
      <ConfigProvider
        theme={theme === 'dark' ? darkTheme : lightTheme}
      >
        {children}
      </ConfigProvider>
    </ThemeContext.Provider>
  )
}

export const useTheme = () => useContext(ThemeContext)
