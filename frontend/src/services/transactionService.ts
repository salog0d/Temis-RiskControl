import type { Transaction, TransactionDetail } from '../types/transaction.types'
import { MOCK_TRANSACTIONS, MOCK_TRANSACTION_DETAIL } from '../mocks/transactions.mock'
import { MOCK_API_DELAY_MS } from '../utils/constants'

export const transactionService = {
  async getTransactions(): Promise<Transaction[]> {
    await new Promise(resolve => setTimeout(resolve, MOCK_API_DELAY_MS))
    return MOCK_TRANSACTIONS
  },

  async getTransactionById(id: string): Promise<TransactionDetail | undefined> {
    await new Promise(resolve => setTimeout(resolve, MOCK_API_DELAY_MS / 2))
    const base = MOCK_TRANSACTIONS.find(t => t.id === id)
    if (!base) return undefined

    // For the first transaction, return full detail; others get base fields
    if (id === 'txn_001') return MOCK_TRANSACTION_DETAIL
    return {
      ...base,
      statementDescriptor: `${base.merchantName} — Statement`,
      signals: base.riskLevel === 'high'
        ? [
            { type: 'unusual_location', label: 'Unusual location detected', severity: 'high' },
            { type: 'high_amount', label: 'Significantly above your baseline', severity: 'high' },
          ]
        : base.riskLevel === 'medium'
          ? [{ type: 'high_amount', label: 'Amount above your typical spending', severity: 'medium' }]
          : [],
    }
  },
}
