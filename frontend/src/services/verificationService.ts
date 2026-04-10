import { MOCK_API_DELAY_MS } from '../utils/constants'

/**
 * Service for submitting step-up verification responses.
 * Real implementation: POST /api/verify
 */
export const verificationService = {
  async submitOTP(_verificationId: string, _code: string): Promise<boolean> {
    await new Promise(resolve => setTimeout(resolve, MOCK_API_DELAY_MS))
    return true // Mock: always succeeds
  },

  async submitPassword(_verificationId: string, _password: string): Promise<boolean> {
    await new Promise(resolve => setTimeout(resolve, MOCK_API_DELAY_MS))
    return true
  },

  async submitMFA(_verificationId: string, _code: string): Promise<boolean> {
    await new Promise(resolve => setTimeout(resolve, MOCK_API_DELAY_MS))
    return true
  },
}
