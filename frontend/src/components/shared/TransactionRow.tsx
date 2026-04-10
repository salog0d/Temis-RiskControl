import { useNavigate } from 'react-router-dom'
import { getRiskDisplay } from '../../utils/riskLevel'
import { formatCurrency } from '../../utils/formatCurrency'
import { Coffee, MoneySend, ShoppingCart, Refresh, GasStation, Card as CardIcon } from 'iconsax-react'
import type { ReactNode } from 'react'
import type { Transaction } from '../../types/transaction.types'
import './TransactionRow.css'

interface TransactionRowProps {
  transaction: Transaction
}

const CATEGORY_ICONS: Record<string, ReactNode> = {
  dining: <Coffee variant="TwoTone" size="24" color="currentColor" />,
  transfer: <MoneySend variant="TwoTone" size="24" color="currentColor" />,
  shopping: <ShoppingCart variant="TwoTone" size="24" color="currentColor" />,
  subscription: <Refresh variant="TwoTone" size="24" color="currentColor" />,
  fuel: <GasStation variant="TwoTone" size="24" color="currentColor" />,
}

export function TransactionRow({ transaction }: TransactionRowProps) {
  const navigate = useNavigate()
  const display = getRiskDisplay(transaction.riskLevel)
  const categoryIcon = CATEGORY_ICONS[transaction.merchantCategory ?? ''] ?? <CardIcon variant="TwoTone" size="24" color="currentColor" />
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
