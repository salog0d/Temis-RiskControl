import { useNavigate } from 'react-router-dom'
import { getRiskDisplay } from '../../utils/riskLevel'
import { formatCurrency } from '../../utils/formatCurrency'
import type { Transaction } from '../../types/transaction.types'
import './TransactionRow.css'

interface TransactionRowProps {
  transaction: Transaction
}

const CATEGORY_ICONS: Record<string, string> = {
  dining: '🍽️',
  transfer: '💸',
  shopping: '🛍️',
  subscription: '🔄',
  fuel: '⛽',
}

export function TransactionRow({ transaction }: TransactionRowProps) {
  const navigate = useNavigate()
  const display = getRiskDisplay(transaction.riskLevel)
  const categoryIcon = CATEGORY_ICONS[transaction.merchantCategory ?? ''] ?? '💳'
  const isBlocked = transaction.status === 'blocked'

  return (
    <button
      className="txn-row"
      onClick={() => navigate(`/transactions/${transaction.id}`)}
    >
      <span className="txn-row-icon">{categoryIcon}</span>
      <div className="txn-row-info">
        <span className="txn-row-merchant">{transaction.merchantName}</span>
        <span className="txn-row-status">
          <span className="txn-row-risk-icon">{display.icon}</span>
          {display.label}
        </span>
      </div>
      <span className={`txn-row-amount ${isBlocked ? 'txn-row-blocked' : ''}`}>
        {isBlocked ? '—' : formatCurrency(transaction.amount)}
      </span>
    </button>
  )
}
