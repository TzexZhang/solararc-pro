import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { shadowService } from '@/services'
import { useMapStore } from '@/store'
import type { ShadowCalculateParams } from '@/types'

export const useShadows = (buildingIds: string[], enabled = true) => {
  const { currentDate, currentHour } = useMapStore()

  const params: ShadowCalculateParams = {
    building_ids: buildingIds,
    date: currentDate,
    hour: currentHour,
    minute: 0
  }

  return useQuery({
    queryKey: ['shadows', buildingIds, currentDate, currentHour],
    queryFn: () => shadowService.calculateShadows(params),
    enabled: enabled && buildingIds.length > 0,
    staleTime: 60000, // 1 minute
    select: (data) => data.shadows
  })
}

export const useShadowComparison = (buildingId: string, hour = 12, enabled = true) => {
  return useQuery({
    queryKey: ['shadowComparison', buildingId, hour],
    queryFn: () => shadowService.compareShadowExtremes(buildingId, hour),
    enabled: enabled && !!buildingId,
    staleTime: 86400000 // 24 hours
  })
}

export const useCalculateShadows = () => {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (params: ShadowCalculateParams) => shadowService.calculateShadows(params),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['shadows'] })
    }
  })
}

export default useShadows
