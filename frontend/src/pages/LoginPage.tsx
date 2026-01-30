import React from 'react'
import { LoginForm } from '@/components/auth'
import './LoginPage.css'

export const LoginPage: React.FC = () => {
  return (
    <div className="login-page">
      <div className="login-background">
        <div className="login-overlay">
          <LoginForm />
        </div>
      </div>
    </div>
  )
}

export default LoginPage
