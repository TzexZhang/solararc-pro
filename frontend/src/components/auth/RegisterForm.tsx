import React from 'react'
import { Form, Input, Button, Card, message } from 'antd'
import { UserOutlined, LockOutlined, MailOutlined } from '@ant-design/icons'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '@/hooks'
import type { RegisterRequest } from '@/types'
import './AuthForm.css'

export const RegisterForm: React.FC = () => {
  const navigate = useNavigate()
  const { register, isLoading } = useAuth()
  const [form] = Form.useForm()

  const handleSubmit = async (values: RegisterRequest) => {
    try {
      await register(values.email, values.password, values.nickname)
      message.success('注册成功，请查收验证邮件')
      navigate('/login')
    } catch (error) {
      // Error is already handled by the auth service
    }
  }

  const validatePassword = (_: any, value: string) => {
    if (!value) {
      return Promise.reject('请输入密码')
    }
    if (value.length < 8) {
      return Promise.reject('密码至少8位')
    }
    if (!/(?=.*[a-zA-Z])(?=.*[0-9])/.test(value)) {
      return Promise.reject('密码必须包含字母和数字')
    }
    return Promise.resolve()
  }

  return (
    <div className="auth-container">
      <Card className="auth-card" title="注册 SolarArc Pro 账号">
        <Form form={form} onFinish={handleSubmit} layout="vertical" size="large">
          <Form.Item
            name="email"
            rules={[
              { required: true, message: '请输入邮箱' },
              { type: 'email', message: '请输入有效的邮箱地址' }
            ]}
          >
            <Input
              prefix={<MailOutlined />}
              placeholder="邮箱"
              autoComplete="email"
            />
          </Form.Item>

          <Form.Item
            name="nickname"
            rules={[{ max: 50, message: '昵称最多50个字符' }]}
          >
            <Input
              prefix={<UserOutlined />}
              placeholder="昵称（可选）"
              autoComplete="nickname"
            />
          </Form.Item>

          <Form.Item
            name="password"
            rules={[{ validator: validatePassword }]}
          >
            <Input.Password
              prefix={<LockOutlined />}
              placeholder="密码（至少8位，包含字母和数字）"
              autoComplete="new-password"
            />
          </Form.Item>

          <Form.Item
            name="confirmPassword"
            dependencies={['password']}
            rules={[
              { required: true, message: '请确认密码' },
              ({ getFieldValue }) => ({
                validator(_, value) {
                  if (!value || getFieldValue('password') === value) {
                    return Promise.resolve()
                  }
                  return Promise.reject(new Error('两次输入的密码不一致'))
                }
              })
            ]}
          >
            <Input.Password
              prefix={<LockOutlined />}
              placeholder="确认密码"
              autoComplete="new-password"
            />
          </Form.Item>

          <Form.Item>
            <Button
              type="primary"
              htmlType="submit"
              loading={isLoading}
              block
            >
              注册
            </Button>
          </Form.Item>

          <div className="auth-footer">
            <span>已有账号？</span>
            <Link to="/login">立即登录</Link>
          </div>
        </Form>
      </Card>
    </div>
  )
}

export default RegisterForm
