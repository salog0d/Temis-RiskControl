export interface Card {
  id: string
  cardholderName: string
  lastFour: string
  isLocked: boolean
  type?: string
  [key: string]: unknown
}
