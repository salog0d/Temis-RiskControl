import type { Account } from '../types/account.types'

export const MOCK_ACCOUNTS: Account[] = [
  {
    id: 'acc_001',
    name: '360 Checking',
    lastFour: '1902',
    balance: 1093.07,
    type: 'checking',
    currency: 'USD',
    status: 'active',
  },
  {
    id: 'acc_002',
    name: 'SAVOR',
    lastFour: '7654',
    balance: 850.06,
    type: 'credit',
    currency: 'USD',
    status: 'active',
  },
  {
    id: 'acc_003',
    name: 'VENTURE',
    lastFour: '7890',
    balance: 523.14,
    type: 'credit',
    currency: 'USD',
    status: 'active',
  },
]
