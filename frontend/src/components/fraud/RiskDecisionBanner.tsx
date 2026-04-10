import { Badge } from '../ui/Badge'
import { getRiskDisplay, getDecisionLabel } from '../../utils/riskLevel'
import { SignalSummary } from './SignalSummary'
import type { Signal } from '../../types/transaction.types'
import './RiskDecisionBanner.css'

interface RiskDecisionBannerProps {
  riskLevel?: string
  riskDecision?: string
  actionTaken?: string
  signals?: Signal[]
  verifiedAt?: string
}

export function RiskDecisionBanner({
  riskLevel,
  riskDecision,
  actionTaken,
  signals = [],
  verifiedAt,
}: RiskDecisionBannerProps) {
  const display = getRiskDisplay(riskLevel)
  const decisionText = getDecisionLabel(riskDecision, actionTaken)

  const badgeVariant = riskLevel === 'high' ? 'danger'
    : riskLevel === 'medium' ? 'warning'
    : 'success'

  return (
    <div className="risk-banner" style={{ borderLeftColor: display.color }}>
      <div className="risk-banner-header">
        <span className="risk-banner-icon">{display.icon}</span>
        <Badge variant={badgeVariant} size="md">{display.label}</Badge>
      </div>
      <p className="risk-banner-text">{decisionText}</p>
      {verifiedAt && (
        <p className="risk-banner-verified">Verified at {verifiedAt}</p>
      )}
      {signals.length > 0 && <SignalSummary signals={signals} />}
    </div>
  )
}
