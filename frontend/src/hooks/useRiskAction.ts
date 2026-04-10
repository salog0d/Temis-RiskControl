import { useState, useCallback } from 'react'
import type { RiskResponse } from '../types/risk.types'
import { riskActionService } from '../services/riskActionService'

/**
 * Central hook connecting user actions to the risk system's response.
 * Manages the verification challenge and blocked overlays.
 */
export function useRiskAction() {
  const [verificationState, setVerificationState] = useState<RiskResponse | null>(null)
  const [showChallenge, setShowChallenge] = useState(false)
  const [showBlocked, setShowBlocked] = useState(false)

  const executeAction = useCallback(async (
    triggerType: string,
    payload: Record<string, unknown>
  ): Promise<boolean> => {
    try {
      const response = await riskActionService.evaluate(triggerType, payload)

      switch (response.decision) {
        case 'approved':
          return true

        case 'step_up_required':
          setVerificationState(response)
          setShowChallenge(true)
          return false

        case 'blocked':
          setVerificationState(response)
          setShowBlocked(true)
          return false

        default:
          return false
      }
    } catch {
      return false
    }
  }, [])

  const dismissChallenge = useCallback(() => {
    setShowChallenge(false)
    setVerificationState(null)
  }, [])

  const dismissBlocked = useCallback(() => {
    setShowBlocked(false)
    setVerificationState(null)
  }, [])

  return {
    executeAction,
    verificationState,
    showChallenge,
    showBlocked,
    dismissChallenge,
    dismissBlocked,
  }
}
