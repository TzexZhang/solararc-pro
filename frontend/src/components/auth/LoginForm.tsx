import React from 'react'
import { Form, Input, Button, Card, message } from 'antd'
import { UserOutlined, LockOutlined } from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '@/hooks'
import type { LoginRequest } from '@/types'
import './AuthForm.css'

export const LoginForm: React.FC = () => {
  const navigate = useNavigate()
  const { login, isLoading } = useAuth()
  const [form] = Form.useForm()

  const handleSubmit = async (values: LoginRequest) => {
    try {
      await login(values.email, values.password)
      message.success('登录成功')
      navigate('/')
    } catch (error) {
      // Error is already handled by the auth service
    }
  }

  return (
    <div className="auth-container">
      <Card className="auth-card" title="登录到 SolarArc Pro">
        <Form form={form} onFinish={handleSubmit} layout="vertical" size="large">
          <Form.Item
            name="email"
            rules={[
              { required: true, message: '请输入邮箱' },
              { type: 'email', message: '请输入有效的邮箱地址' }
            ]}
          >
            <Input
              prefix={<UserOutlined />}
              placeholder="邮箱"
              autoComplete="email"
            />
          </Form.Item>

          <Form.Item
            name="password"
            rules={[
              { required: true, message: '请输入密码' },
              { min: 8, message: '密码至少8位' }
            ]}
          >
            <Input.Password
              prefix={<LockOutlined />}
              placeholder="密码"
              autoComplete="current-password"
            />
          </Form.Item>

          <Form.Item>
            <Button
              type="primary"
              htmlType="submit"
              loading={isLoading}
              block
            >
              登录
            </Button>
          </Form.Item>

          <div className="auth-footer">
            <a href="/forgot-password">忘记密码？</a>
            <span>|</span>
            <a href="/register">注册账号</a>
          </div>
        </Form>
      </Card>
    </div>
  )
}

export default LoginForm
