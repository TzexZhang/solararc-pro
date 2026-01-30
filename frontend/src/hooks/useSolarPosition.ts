import { useQuery } from '@tanstack/react-query'
import { solarService } from '@/services'
import { useMapStore } from '@/store'
import dayjs from 'dayjs'

export const useSolarPosition = (enabled = true) => {
  const { viewport, currentDate, currentHour } = useMapStore()

  return useQuery({
    queryKey: ['solarPosition', viewport.latitude, viewport.longitude, currentDate, currentHour],
    queryFn: () =>
      solarService.getSolarPosition({
        lat: viewport.latitude,
        lng: viewport.longitude,
        date: currentDate,
        hour: currentHour,
        minute: 0
      }),
    enabled: enabled && !!viewport.latitude && !!viewport.longitude,
    staleTime: 60000, // 1 minute
    refetchOnWindowFocus: false
  })
}

export const useDailySolarPositions = (date?: string) => {
  const { viewport, currentDate } = useMapStore()
  const targetDate = date || currentDate

  return useQuery({
    queryKey: ['dailySolarPositions', viewport.latitude, viewport.longitude, targetDate],
    queryFn: () =>
      solarService.getDailySolarPositions(viewport.latitude, viewport.longitude, targetDate),
    enabled: !!viewport.latitude && !!viewport.longitude,
    staleTime: 300000, // 5 minutes
    refetchOnWindowFocus: false
  })
}

export default useSolarPosition
