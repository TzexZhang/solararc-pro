import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { buildingService } from '@/services'
import { useMapStore } from '@/store'
import type { Building } from '@/types'
import { message } from 'antd'

export const useBuildingsInBounds = (bounds: any, enabled = true) => {
  const { showShadows, currentDate, currentHour } = useMapStore()

  return useQuery({
    queryKey: ['buildings', bounds, showShadows, currentDate, currentHour],
    queryFn: () =>
      buildingService.getBuildingsInBounds({
        ...bounds,
        include_shadow: showShadows,
        analysis_date: currentDate,
        analysis_hour: currentHour
      }),
    enabled:
      enabled &&
      !!bounds &&
      !!bounds.min_lat &&
      !!bounds.max_lat &&
      !!bounds.min_lng &&
      !!bounds.max_lng,
    staleTime: 300000, // 5 minutes
    select: (data) => data.buildings
  })
}

export const useBuilding = (id: string, enabled = true) => {
  return useQuery({
    queryKey: ['building', id],
    queryFn: () => buildingService.getBuildingById(id),
    enabled: enabled && !!id,
    staleTime: 600000 // 10 minutes
  })
}

export const useImportBuildings = () => {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (params: { file: File; city?: string }) => buildingService.importBuildings(params),
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['buildings'] })
      message.success(
        `导入成功：${data.success_count} 个建筑${data.failed_count > 0 ? `，失败 ${data.failed_count} 个` : ''}`
      )
    },
    onError: (error: any) => {
      message.error(`导入失败：${error.message || '未知错误'}`)
    }
  })
}

export const useDeleteBuilding = () => {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (id: string) => buildingService.deleteBuilding(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['buildings'] })
      message.success('删除成功')
    },
    onError: (error: any) => {
      message.error(`删除失败：${error.message || '未知错误'}`)
    }
  })
}

export default useBuildingsInBounds
