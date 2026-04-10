export interface RiskDisplay {
  label: string
  color: string
  bgColor: string
  icon: string
}

const RISK_DISPLAY_MAP: Record<string, RiskDisplay> = {
  low: {
    label: 'Approved',
    color: 'var(--color-risk-low)',
    bgColor: 'var(--color-risk-low-bg)',
    icon: '✅',
  },
  medium: {
    label: 'Verified',
    color: 'var(--color-risk-medium)',
    bgColor: 'var(--color-risk-medium-bg)',
    icon: '🔐',
  },
  high: {
    label: 'Blocked',
    color: 'var(--color-risk-high)',
    bgColor: 'var(--color-risk-high-bg)',
    icon: '🚫',
  },
  critical: {
    label: 'Frozen',
    color: 'var(--color-risk-critical)',
    bgColor: 'var(--color-risk-critical-bg)',
    icon: '🔒',
  },
}

const DEFAULT_DISPLAY: RiskDisplay = {
  label: 'Unknown',
  color: 'var(--text-secondary)',
  bgColor: 'transparent',
  icon: '❓',
}

/**
 * Maps a risk level string to display properties.
 * Falls back gracefully for unknown values to support open-ended backend.
 */
export function getRiskDisplay(riskLevel?: string): RiskDisplay {
  if (!riskLevel) return RISK_DISPLAY_MAP.low
  return RISK_DISPLAY_MAP[riskLevel] ?? DEFAULT_DISPLAY
}

/** Maps a decision string to a human-readable action label */
export function getDecisionLabel(decision?: string, actionTaken?: string): string {
  switch (decision) {
    case 'approved':
      return 'Approved — No issues detected'
    case 'step_up_required':
      return getStepUpLabel(actionTaken)
    case 'blocked':
      return 'Blocked — This action was stopped for your security'
    default:
      return 'Processing'
  }
}

function getStepUpLabel(actionTaken?: string): string {
  switch (actionTaken) {
    case 'otp_sent':
      return 'Verification required — OTP sent'
    case 'mfa_required':
      return 'Verification required — MFA'
    case 'password_required':
      return 'Re-enter password to continue'
    case 'biometric_required':
      return 'Biometric verification required'
    case 'account_frozen':
      return 'Account temporarily frozen'
    default:
      return 'Additional verification required'
  }
}
