import type { Signal } from './transaction.types'

export interface ActivityEvent {
  id: string
  timestamp: string
  triggerType: string
  triggerDescription: string
  riskLevel?: string
  decision: string
  actionTaken: string
  actionLabel: string
  resolved: boolean
  signals?: Signal[]
  relatedTransactionId?: string
  [key: string]: unknown
}
