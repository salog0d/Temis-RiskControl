import type { Signal } from './transaction.types'

export type RiskDecision = 'approved' | 'step_up_required' | 'blocked'

export type ActionTaken =
  | 'none'
  | 'otp_sent'
  | 'mfa_required'
  | 'password_required'
  | 'biometric_required'
  | 'blocked'
  | 'account_frozen'

export interface RiskResponse {
  decision: RiskDecision
  actionTaken: ActionTaken
  signals?: Signal[]
  verificationId?: string
  message?: string
}

export interface VerificationRequest {
  verificationId: string
  method: string
  code?: string
  password?: string
  [key: string]: unknown
}
