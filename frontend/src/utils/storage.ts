/**
 * Local storage wrapper with error handling and type safety
 */

export const storage = {
  // Get item from localStorage
  get<T = any>(key: string): T | null {
    try {
      const item = window.localStorage.getItem(key)
      if (item === null) return null
      return JSON.parse(item) as T
    } catch (error) {
      console.error(`Error reading from localStorage key "${key}":`, error)
      return null
    }
  },

  // Set item in localStorage
  set(key: string, value: any): boolean {
    try {
      window.localStorage.setItem(key, JSON.stringify(value))
      return true
    } catch (error) {
      console.error(`Error writing to localStorage key "${key}":`, error)
      return false
    }
  },

  // Remove item from localStorage
  remove(key: string): boolean {
    try {
      window.localStorage.removeItem(key)
      return true
    } catch (error) {
      console.error(`Error removing localStorage key "${key}":`, error)
      return false
    }
  },

  // Clear all items from localStorage
  clear(): boolean {
    try {
      window.localStorage.clear()
      return true
    } catch (error) {
      console.error('Error clearing localStorage:', error)
      return false
    }
  },

  // Check if key exists
  has(key: string): boolean {
    return window.localStorage.getItem(key) !== null
  }
}

/**
 * Session storage wrapper (same API as localStorage wrapper)
 */
export const sessionStorage = {
  get<T = any>(key: string): T | null {
    try {
      const item = window.sessionStorage.getItem(key)
      if (item === null) return null
      return JSON.parse(item) as T
    } catch (error) {
      console.error(`Error reading from sessionStorage key "${key}":`, error)
      return null
    }
  },

  set(key: string, value: any): boolean {
    try {
      window.sessionStorage.setItem(key, JSON.stringify(value))
      return true
    } catch (error) {
      console.error(`Error writing to sessionStorage key "${key}":`, error)
      return false
    }
  },

  remove(key: string): boolean {
    try {
      window.sessionStorage.removeItem(key)
      return true
    } catch (error) {
      console.error(`Error removing sessionStorage key "${key}":`, error)
      return false
    }
  },

  clear(): boolean {
    try {
      window.sessionStorage.clear()
      return true
    } catch (error) {
      console.error('Error clearing sessionStorage:', error)
      return false
    }
  },

  has(key: string): boolean {
    return window.sessionStorage.getItem(key) !== null
  }
}

export default storage
