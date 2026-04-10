import type { Account } from '../types/account.types'
import type { Transaction } from '../types/transaction.types'
import { MOCK_ACCOUNTS } from '../mocks/accounts.mock'
import { MOCK_TRANSACTIONS } from '../mocks/transactions.mock'
import { MOCK_API_DELAY_MS } from '../utils/constants'

/** Mock account service — swap to apiClient calls when backend is ready */
export const accountService = {
  async getAccounts(): Promise<Account[]> {
    await new Promise(resolve => setTimeout(resolve, MOCK_API_DELAY_MS))
    return MOCK_ACCOUNTS
  },

  async getAccountById(id: string): Promise<Account | undefined> {
    await new Promise(resolve => setTimeout(resolve, MOCK_API_DELAY_MS / 2))
    return MOCK_ACCOUNTS.find(a => a.id === id)
  },

  async getAccountTransactions(accountId: string): Promise<Transaction[]> {
    await new Promise(resolve => setTimeout(resolve, MOCK_API_DELAY_MS))
    return MOCK_TRANSACTIONS.filter(t => t.accountId === accountId)
  },
}
