import type { Card } from '../types/card.types'

export const MOCK_CARDS: Card[] = [
  {
    id: 'card_001',
    cardholderName: 'Beth S. (Your card)',
    lastFour: '1234',
    isLocked: true,
    type: 'debit',
  },
  {
    id: 'card_002',
    cardholderName: 'Richie H.',
    lastFour: '5678',
    isLocked: false,
    type: 'debit',
  },
]
