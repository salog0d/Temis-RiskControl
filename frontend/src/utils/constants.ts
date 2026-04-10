/** Named timing constants to avoid magic numbers */
export const DEBOUNCE_DELAY_MS = 500
export const MOCK_API_DELAY_MS = 800
export const OTP_CODE_LENGTH = 6
export const OTP_RESEND_COOLDOWN_SEC = 60
export const MAX_RETRIES = 3

/** Route paths */
export const ROUTES = {
  LOGIN: '/login',
  DASHBOARD: '/dashboard',
  ACCOUNT_DETAIL: '/accounts/:id',
  TRANSACTION_DETAIL: '/transactions/:id',
  SECURITY: '/security',
  ACTIVITY: '/activity',
  SETTINGS: '/settings',
} as const

/** Account type → CSS gradient mapping */
export const ACCOUNT_GRADIENTS: Record<string, string> = {
  checking: 'var(--gradient-checking)',
  savings: 'var(--gradient-savings)',
  credit: 'var(--gradient-credit)',
}
