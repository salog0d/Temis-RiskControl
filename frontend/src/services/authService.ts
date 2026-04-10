import type { User } from '../types/user.types'
import { MOCK_USER } from '../mocks/user.mock'
import { MOCK_API_DELAY_MS } from '../utils/constants'

/**
 * Auth service — currently mock, designed for single-file swap to real endpoints.
 *
 * Real implementation would call:
 *   POST /api/auth/login
 *   POST /api/auth/logout
 *   GET  /api/auth/me
 */
export const authService = {
  async login(_email: string, _password: string): Promise<{ user: User; token: string }> {
    await new Promise(resolve => setTimeout(resolve, MOCK_API_DELAY_MS))
    const token = 'mock-jwt-token-' + Date.now()
    localStorage.setItem('token', token)
    return { user: MOCK_USER, token }
  },

  async logout(): Promise<void> {
    localStorage.removeItem('token')
  },

  getToken(): string | null {
    return localStorage.getItem('token')
  },

  isAuthenticated(): boolean {
    return !!localStorage.getItem('token')
  },

  async getCurrentUser(): Promise<User> {
    await new Promise(resolve => setTimeout(resolve, MOCK_API_DELAY_MS / 2))
    return MOCK_USER
  },
}
