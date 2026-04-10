export interface Account {
  id: string
  name: string
  lastFour: string
  balance: number
  type: string
  currency?: string
  status?: string
  [key: string]: unknown
}
