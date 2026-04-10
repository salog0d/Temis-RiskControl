import type { RiskResponse } from '../types/risk.types'
import { MOCK_API_DELAY_MS } from '../utils/constants'

/**
 * Service that evaluates user actions against the risk engine.
 * Real implementation: POST /api/actions/evaluate
 */
export const riskActionService = {
  async evaluate(
    _triggerType: string,
    _payload: Record<string, unknown>
  ): Promise<RiskResponse> {
    await new Promise(resolve => setTimeout(resolve, MOCK_API_DELAY_MS))

    // Mock: return approved by default
    // In the real system, the backend risk/decision/action agents determine this
    return {
      decision: 'approved',
      actionTaken: 'none',
      message: 'Action approved',
    }
  },
}
