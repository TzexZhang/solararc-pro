import dayjs from 'dayjs'

/**
 * Format date to display string
 */
export const formatDate = (date: string | Date, format = 'YYYY-MM-DD'): string => {
  return dayjs(date).format(format)
}

/**
 * Format date time to display string
 */
export const formatDateTime = (dateTime: string | Date, format = 'YYYY-MM-DD HH:mm:ss'): string => {
  return dayjs(dateTime).format(format)
}

/**
 * Format time to display string (HH:mm)
 */
export const formatTime = (time: string | Date, format = 'HH:mm'): string => {
  return dayjs(time).format(format)
}

/**
 * Format number with thousand separator
 */
export const formatNumber = (num: number, decimals = 2): string => {
  return num.toLocaleString('zh-CN', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals
  })
}

/**
 * Format area in square meters
 */
export const formatArea = (area: number): string => {
  if (area >= 10000) {
    return `${formatNumber(area / 10000, 2)} 万平方米`
  }
  return `${formatNumber(area, 2)} 平方米`
}

/**
 * Format percentage
 */
export const formatPercent = (value: number, decimals = 1): string => {
  return `${value.toFixed(decimals)}%`
}

/**
 * Format decimal degrees to DMS (Degrees Minutes Seconds)
 */
export const toDMS = (decimalDegrees: number): string => {
  const degrees = Math.floor(decimalDegrees)
  const minutesFloat = (decimalDegrees - degrees) * 60
  const minutes = Math.floor(minutesFloat)
  const seconds = ((minutesFloat - minutes) * 60).toFixed(1)

  return `${degrees}°${minutes}'${seconds}"`
}

/**
 * Format coordinate
 */
export const formatCoordinate = (lat: number, lng: number): string => {
  return `${lat.toFixed(6)}, ${lng.toFixed(6)}`
}

/**
 * Format building score to grade
 */
export const scoreToGrade = (score: number): { label: string; color: string } => {
  if (score >= 80) {
    return { label: '优', color: '#52c41a' }
  } else if (score >= 60) {
    return { label: '良', color: '#1890ff' }
  } else if (score >= 40) {
    return { label: '中', color: '#faad14' }
  } else {
    return { label: '差', color: '#f5222d' }
  }
}

/**
 * Format file size
 */
export const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 B'

  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))

  return `${(bytes / Math.pow(k, i)).toFixed(2)} ${sizes[i]}`
}

/**
 * Format duration (seconds to human readable)
 */
export const formatDuration = (seconds: number): string => {
  if (seconds < 60) {
    return `${seconds}秒`
  } else if (seconds < 3600) {
    const minutes = Math.floor(seconds / 60)
    return `${minutes}分钟`
  } else {
    const hours = Math.floor(seconds / 3600)
    const minutes = Math.floor((seconds % 3600) / 60)
    return minutes > 0 ? `${hours}小时${minutes}分钟` : `${hours}小时`
  }
}

/**
 * Truncate text with ellipsis
 */
export const truncate = (text: string, maxLength: number): string => {
  if (text.length <= maxLength) return text
  return text.substring(0, maxLength) + '...'
}
