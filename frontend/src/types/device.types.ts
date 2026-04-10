export interface Device {
  id: string
  name: string
  lastSeen: string
  trustLevel: string
  [key: string]: unknown
}
