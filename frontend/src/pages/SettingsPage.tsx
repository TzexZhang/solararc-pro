import React from 'react'
import { Layout, Card, Form, Input, Button, Switch, Divider, Space, message, Select } from 'antd'
import { Header, Sidebar, Footer } from '@/components/layout'
import { useMapStore } from '@/store'
import { useAuthStore } from '@/store'
import { useNavigate } from 'react-router-dom'
import { useChangePassword } from '@/hooks'
import './SettingsPage.css'

const { Content } = Layout
const { Item: FormItem } = Form
const { TextArea } = Input

export const SettingsPage: React.FC = () => {
  const { sidebarCollapsed } = useMapStore()
  const { user, logout } = useAuthStore()
  const { theme, toggleTheme } = useAppStore()
  const navigate = useNavigate()
  const changePasswordMutation = useChangePassword()

  const handleProfileUpdate = (values: any) => {
    message.success('个人信息更新成功')
  }

  const handlePasswordChange = async (values: any) => {
    try {
      await changePasswordMutation.mutateAsync({
        oldPassword: values.oldPassword,
        newPassword: values.newPassword
      })

      message.success('密码修改成功，请重新登录')

      // 清除状态并跳转到登录页
      setTimeout(async () => {
        await logout()
        navigate('/login')
      }, 1000)
    } catch (error: any) {
      console.error('密码修改失败:', error)
      message.error(error.response?.data?.detail || '密码修改失败')
    }
  }

  const handleSettingsChange = (values: any) => {
    message.success('设置保存成功')
  }

  return (
    <Layout className="settings-page">
      <Header />
      <Layout>
        <Sidebar collapsed={sidebarCollapsed} />
        <Layout
          style={{
            marginLeft: sidebarCollapsed ? 80 : 240,
            transition: 'margin-left 0.2s'
          }}
        >
          <Content className="content">
            <div className="settings-content">
              <h1 className="page-title">设置</h1>

              <Space direction="vertical" size="large" style={{ width: '100%' }}>
                {/* Profile Settings */}
                <Card title="个人信息" className="settings-card">
                  <Form
                    layout="vertical"
                    initialValues={user ? { email: user.email, nickname: user.nickname } : {}}
                    onFinish={handleProfileUpdate}
                  >
                    <FormItem label="邮箱" name="email">
                      <Input disabled />
                    </FormItem>
                    <FormItem label="昵称" name="nickname">
                      <Input placeholder="请输入昵称" />
                    </FormItem>
                    <FormItem>
                      <Button type="primary" htmlType="submit">
                        更新个人信息
                      </Button>
                    </FormItem>
                  </Form>
                </Card>

                {/* Password Change */}
                <Card title="修改密码" className="settings-card">
                  <Form layout="vertical" onFinish={handlePasswordChange}>
                    <FormItem label="当前密码" name="oldPassword" rules={[{ required: true }]}>
                      <Input.Password placeholder="请输入当前密码" />
                    </FormItem>
                    <FormItem label="新密码" name="newPassword" rules={[{ required: true, min: 8 }]}>
                      <Input.Password placeholder="请输入新密码（至少8位）" />
                    </FormItem>
                    <FormItem
                      label="确认密码"
                      name="confirmPassword"
                      dependencies={['newPassword']}
                      rules={[
                        { required: true },
                        ({ getFieldValue }) => ({
                          validator(_, value) {
                            if (!value || getFieldValue('newPassword') === value) {
                              return Promise.resolve()
                            }
                            return Promise.reject(new Error('两次输入的密码不一致'))
                          }
                        })
                      ]}
                    >
                      <Input.Password placeholder="请再次输入新密码" />
                    </FormItem>
                    <FormItem>
                      <Button type="primary" htmlType="submit">
                        修改密码
                      </Button>
                    </FormItem>
                  </Form>
                </Card>

                {/* App Settings */}
                <Card title="应用设置" className="settings-card">
                  <Form layout="vertical" onFinish={handleSettingsChange}>
                    <FormItem label="深色模式">
                      <Switch checked={theme === 'dark'} onChange={toggleTheme} />
                    </FormItem>
                    <FormItem label="推送通知">
                      <Switch defaultChecked />
                    </FormItem>
                    <FormItem label="自动保存">
                      <Switch defaultChecked />
                    </FormItem>
                    <FormItem label="数据刷新频率">
                      <Select defaultValue="60">
                        <Select.Option value="30">30秒</Select.Option>
                        <Select.Option value="60">1分钟</Select.Option>
                        <Select.Option value="300">5分钟</Select.Option>
                        <Select.Option value="600">10分钟</Select.Option>
                      </Select>
                    </FormItem>
                    <FormItem>
                      <Button type="primary" htmlType="submit">
                        保存设置
                      </Button>
                    </FormItem>
                  </Form>
                </Card>

                {/* About */}
                <Card title="关于" className="settings-card">
                  <Space direction="vertical">
                    <div><strong>SolarArc Pro</strong></div>
                    <div>版本: 1.0.0</div>
                    <div>高性能城市日照分析与可视化模拟平台</div>
                    <Divider />
                    <div>© 2026 SolarArc Pro. All rights reserved.</div>
                  </Space>
                </Card>
              </Space>
            </div>
          </Content>
          <Footer />
        </Layout>
      </Layout>
    </Layout>
  )
}

export default SettingsPage
