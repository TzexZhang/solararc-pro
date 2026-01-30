import React from 'react'
import { Layout, Table, Button, Space, Tag, Card } from 'antd'
import { EyeOutlined, DeleteOutlined, DownloadOutlined } from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'
import { Header, Sidebar, Footer } from '@/components/layout'
import { useReports, useDeleteReport, useExportReport } from '@/hooks'
import { useMapStore } from '@/store'
import type { AnalysisReport } from '@/types'
import { formatDate, scoreToGrade } from '@/utils/format'
import './ReportsPage.css'

const { Content } = Layout

export const ReportsPage: React.FC = () => {
  const navigate = useNavigate()
  const { sidebarCollapsed } = useMapStore()
  const { data: reports, isLoading } = useReports({}, true)
  const { mutate: deleteReport } = useDeleteReport()
  const { mutate: exportReport } = useExportReport()

  const handleView = (record: AnalysisReport) => {
    navigate(`/reports/${record.id}`)
  }

  const handleDelete = (id: string) => {
    if (confirm('确定要删除此报告吗？')) {
      deleteReport(id)
    }
  }

  const handleExport = (id: string, format: string) => {
    exportReport({ reportId: id, format })
  }

  const getStatusTag = (status: string) => {
    const statusMap: Record<string, { color: string; label: string }> = {
      processing: { color: 'processing', label: '处理中' },
      completed: { color: 'success', label: '已完成' },
      failed: { color: 'error', label: '失败' }
    }
    const statusInfo = statusMap[status] || { color: 'default', label: status }
    return <Tag color={statusInfo.color}>{statusInfo.label}</Tag>
  }

  const columns = [
    {
      title: '报告名称',
      dataIndex: 'name',
      key: 'name',
      ellipsis: true
    },
    {
      title: '分析类型',
      dataIndex: 'analysis_type',
      key: 'analysis_type',
      render: (type: string) => {
        const typeMap: Record<string, string> = {
          daily: '日分析',
          seasonal: '季节分析',
          custom: '自定义'
        }
        return typeMap[type] || type
      }
    },
    {
      title: '创建时间',
      dataIndex: 'created_at',
      key: 'created_at',
      render: (date: string) => formatDate(date)
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => getStatusTag(status)
    },
    {
      title: '操作',
      key: 'action',
      render: (_: any, record: AnalysisReport) => (
        <Space size="small">
          <Button
            type="link"
            icon={<EyeOutlined />}
            onClick={() => handleView(record)}
            size="small"
          >
            查看
          </Button>
          <Button
            type="link"
            icon={<DownloadOutlined />}
            onClick={() => handleExport(record.id, 'pdf')}
            size="small"
          >
            导出
          </Button>
          <Button
            type="link"
            danger
            icon={<DeleteOutlined />}
            onClick={() => handleDelete(record.id)}
            size="small"
          >
            删除
          </Button>
        </Space>
      )
    }
  ]

  return (
    <Layout className="reports-page">
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
            <div className="reports-content">
              <div className="page-header">
                <h1 className="page-title">分析报告</h1>
                <Button type="primary" onClick={() => navigate('/analysis/new')}>
                  创建新报告
                </Button>
              </div>

              <Card className="reports-table-card">
                <Table
                  columns={columns}
                  dataSource={reports}
                  rowKey="id"
                  loading={isLoading}
                  pagination={{
                    pageSize: 20,
                    showSizeChanger: true,
                    showTotal: (total) => `共 ${total} 条记录`
                  }}
                />
              </Card>
            </div>
          </Content>
          <Footer />
        </Layout>
      </Layout>
    </Layout>
  )
}

export default ReportsPage
