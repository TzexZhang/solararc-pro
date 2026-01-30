import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { analysisService } from '@/services'
import type { CreateReportParams, ReportListParams } from '@/types'
import { message } from 'antd'

export const useReports = (params?: ReportListParams, enabled = true) => {
  return useQuery({
    queryKey: ['reports', params],
    queryFn: () => analysisService.getReports(params),
    enabled,
    staleTime: 300000, // 5 minutes
    select: (data) => data.reports
  })
}

export const useReport = (id: string, enabled = true) => {
  return useQuery({
    queryKey: ['report', id],
    queryFn: () => analysisService.getReportById(id),
    enabled: enabled && !!id,
    staleTime: 600000 // 10 minutes
  })
}

export const useCreateReport = () => {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (params: CreateReportParams) => analysisService.createReport(params),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['reports'] })
      message.success('分析报告创建成功')
    },
    onError: (error: any) => {
      message.error(`创建失败：${error.message || '未知错误'}`)
    }
  })
}

export const useDeleteReport = () => {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (id: string) => analysisService.deleteReport(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['reports'] })
      message.success('报告删除成功')
    },
    onError: (error: any) => {
      message.error(`删除失败：${error.message || '未知错误'}`)
    }
  })
}

export const useBuildingScores = (reportId: string, enabled = true) => {
  return useQuery({
    queryKey: ['buildingScores', reportId],
    queryFn: () => analysisService.getBuildingScores(reportId),
    enabled: enabled && !!reportId,
    staleTime: 300000
  })
}

export const useChartData = (reportId: string, chartType: string, enabled = true) => {
  return useQuery({
    queryKey: ['chartData', reportId, chartType],
    queryFn: () => analysisService.getChartData(reportId, chartType),
    enabled: enabled && !!reportId && !!chartType,
    staleTime: 300000
  })
}

export const useExportReport = () => {
  return useMutation({
    mutationFn: ({ reportId, format }: { reportId: string; format: string }) =>
      analysisService.exportReport(reportId, format),
    onSuccess: (blob: Blob) => {
      // Create download link
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `report.${blob.type.includes('pdf') ? 'pdf' : 'xlsx'}`
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
      message.success('报告导出成功')
    },
    onError: (error: any) => {
      message.error(`导出失败：${error.message || '未知错误'}`)
    }
  })
}

export default useReports
