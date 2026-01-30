/**
 * Coordinate system conversion utilities
 * Supports WGS84, GCJ-02 (China), BD-09 (Baidu)
 */

export interface Coordinate {
  lng: number
  lat: number
}

/**
 * Convert WGS84 to GCJ-02 (Mars coordinates)
 */
export function wgs84ToGcj02(lng: number, lat: number): Coordinate {
  const a = 6378245.0
  const ee = 0.00669342162296594323

  if (outOfChina(lng, lat)) {
    return { lng, lat }
  }

  let dLat = transformLat(lng - 105.0, lat - 35.0)
  let dLng = transformLng(lng - 105.0, lat - 35.0)
  const radLat = (lat / 180.0) * Math.PI
  let magic = Math.sin(radLat)
  magic = 1 - ee * magic * magic
  const sqrtMagic = Math.sqrt(magic)
  dLat = (dLat * 180.0) / (((a * (1 - ee)) / (magic * sqrtMagic)) * Math.PI)
  dLng = (dLng * 180.0) / ((a / sqrtMagic) * Math.cos(radLat) * Math.PI)
  const mgLat = lat + dLat
  const mgLng = lng + dLng

  return { lng: mgLng, lat: mgLat }
}

/**
 * Convert GCJ-02 to WGS84
 */
export function gcj02ToWgs84(lng: number, lat: number): Coordinate {
  if (outOfChina(lng, lat)) {
    return { lng, lat }
  }

  const gcj = wgs84ToGcj02(lng, lat)
  const dLat = gcj.lat - lat
  const dLng = gcj.lng - lng
  return { lng: lng - dLng, lat: lat - dLat }
}

/**
 * Convert GCJ-02 to BD-09 (Baidu coordinates)
 */
export function gcj02ToBd09(lng: number, lat: number): Coordinate {
  const x_pi = (3.14159265358979324 * 3000.0) / 180.0
  const z = Math.sqrt(lng * lng + lat * lat) + 0.00002 * Math.sin(lat * x_pi)
  const theta = Math.atan2(lat, lng) + 0.000003 * Math.cos(lng * x_pi)
  const bdLng = z * Math.cos(theta) + 0.0065
  const bdLat = z * Math.sin(theta) + 0.006
  return { lng: bdLng, lat: bdLat }
}

/**
 * Convert BD-09 to GCJ-02
 */
export function bd09ToGcj02(lng: number, lat: number): Coordinate {
  const x_pi = (3.14159265358979324 * 3000.0) / 180.0
  let x = lng - 0.0065
  let y = lat - 0.006
  const z = Math.sqrt(x * x + y * y) - 0.00002 * Math.sin(y * x_pi)
  const theta = Math.atan2(y, x) - 0.000003 * Math.cos(x * x_pi)
  const gcjLng = z * Math.cos(theta)
  const gcjLat = z * Math.sin(theta)
  return { lng: gcjLng, lat: gcjLat }
}

/**
 * Convert WGS84 to BD-09
 */
export function wgs84ToBd09(lng: number, lat: number): Coordinate {
  const gcj = wgs84ToGcj02(lng, lat)
  return gcj02ToBd09(gcj.lng, gcj.lat)
}

/**
 * Convert BD-09 to WGS84
 */
export function bd09ToWgs84(lng: number, lat: number): Coordinate {
  const gcj = bd09ToGcj02(lng, lat)
  return gcj02ToWgs84(gcj.lng, gcj.lat)
}

/**
 * Transform latitude
 */
function transformLat(lng: number, lat: number): number {
  let ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + 0.1 * lng * lat + 0.2 * Math.sqrt(Math.abs(lng))
  ret += ((20.0 * Math.sin(6.0 * lng * Math.PI) + 20.0 * Math.sin(2.0 * lng * Math.PI)) * 2.0) / 3.0
  ret += ((20.0 * Math.sin(lat * Math.PI) + 40.0 * Math.sin((lat / 3.0) * Math.PI)) * 2.0) / 3.0
  ret += ((160.0 * Math.sin((lat / 12.0) * Math.PI) + 320 * Math.sin((lat * Math.PI) / 30.0)) * 2.0) / 3.0
  return ret
}

/**
 * Transform longitude
 */
function transformLng(lng: number, lat: number): number {
  let ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + 0.1 * lng * lat + 0.1 * Math.sqrt(Math.abs(lng))
  ret += ((20.0 * Math.sin(6.0 * lng * Math.PI) + 20.0 * Math.sin(2.0 * lng * Math.PI)) * 2.0) / 3.0
  ret += ((20.0 * Math.sin(lng * Math.PI) + 40.0 * Math.sin((lng / 3.0) * Math.PI)) * 2.0) / 3.0
  ret += ((150.0 * Math.sin((lng / 12.0) * Math.PI) + 300.0 * Math.sin((lng / 30.0) * Math.PI)) * 2.0) / 3.0
  return ret
}

/**
 * Check if coordinates are out of China
 */
function outOfChina(lng: number, lat: number): boolean {
  return lng < 72.004 || lng > 137.8347 || lat < 0.8293 || lat > 55.8271
}

/**
 * Calculate distance between two coordinates (in meters)
 * Uses Haversine formula
 */
export function calculateDistance(coord1: Coordinate, coord2: Coordinate): number {
  const R = 6371000 // Earth's radius in meters
  const φ1 = (coord1.lat * Math.PI) / 180
  const φ2 = (coord2.lat * Math.PI) / 180
  const Δφ = ((coord2.lat - coord1.lat) * Math.PI) / 180
  const Δλ = ((coord2.lng - coord1.lng) * Math.PI) / 180

  const a = Math.sin(Δφ / 2) * Math.sin(Δφ / 2) + Math.cos(φ1) * Math.cos(φ2) * Math.sin(Δλ / 2) * Math.sin(Δλ / 2)
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))

  return R * c
}

/**
 * Calculate bounding box from center point and radius
 */
export function calculateBoundingBox(center: Coordinate, radiusInKm: number) {
  const latDiff = (radiusInKm / 111) * 1 // 1 degree latitude ≈ 111 km
  const lngDiff = (radiusInKm / (111 * Math.cos((center.lat * Math.PI) / 180))) * 1

  return {
    minLat: center.lat - latDiff,
    maxLat: center.lat + latDiff,
    minLng: center.lng - lngDiff,
    maxLng: center.lng + lngDiff
  }
}
