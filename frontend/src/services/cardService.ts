import type { Card } from '../types/card.types'
import { MOCK_CARDS } from '../mocks/cards.mock'
import { MOCK_API_DELAY_MS } from '../utils/constants'

export const cardService = {
  async getCards(): Promise<Card[]> {
    await new Promise(resolve => setTimeout(resolve, MOCK_API_DELAY_MS))
    return [...MOCK_CARDS]
  },

  async toggleLock(cardId: string): Promise<Card> {
    await new Promise(resolve => setTimeout(resolve, MOCK_API_DELAY_MS))
    const card = MOCK_CARDS.find(c => c.id === cardId)
    if (!card) throw new Error('Card not found')
    // In mock, mutate and return (real version: PATCH /api/cards/:id/lock)
    card.isLocked = !card.isLocked
    return { ...card }
  },
}
