import React from 'react'
import { RegisterForm } from '@/components/auth'
import './LoginPage.css'

export const RegisterPage: React.FC = () => {
  return (
    <div className="login-page">
      <div className="login-background">
        <div className="login-overlay">
          <RegisterForm />
        </div>
      </div>
    </div>
  )
}

export default RegisterPage
