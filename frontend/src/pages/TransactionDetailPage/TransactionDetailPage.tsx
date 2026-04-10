import { useParams } from 'react-router-dom'
import { Phone, Globe, AlertTriangle } from 'lucide-react'
import { useQuery } from '../../hooks/useQuery'
import { transactionService } from '../../services/transactionService'
import { PageHeader } from '../../components/layout/PageHeader'
import { RiskDecisionBanner } from '../../components/fraud/RiskDecisionBanner'
import { PageSpinner } from '../../components/ui/Spinner'
import { formatCurrency } from '../../utils/formatCurrency'
import { formatDateFull } from '../../utils/formatDate'
import type { TransactionDetail } from '../../types/transaction.types'
import './TransactionDetailPage.css'

export function TransactionDetailPage() {
  const { id } = useParams<{ id: string }>()

  const { data: transaction, loading } = useQuery<TransactionDetail | undefined>(
    `txn-${id}`,
    () => transactionService.getTransactionById(id!)
  )

  if (loading) return <PageSpinner />
  if (!transaction) return <div className="page">Transaction not found</div>

  const isBlocked = transaction.status === 'blocked'

  return (
    <div className="txn-detail-page">
      <PageHeader title="Transaction Details" showBack />

      <div className="txn-detail-content">
        {/* Amount + Date */}
        <div className="txn-detail-amount-section">
          <h2 className={`txn-detail-amount ${isBlocked ? 'txn-detail-amount-blocked' : ''}`}>
            {formatCurrency(transaction.amount)}
          </h2>
          <p className="txn-detail-date">
            {isBlocked ? 'Blocked' : 'Posted'} on {formatDateFull(transaction.date)}
          </p>
        </div>

        <div className="divider" />

        {/* Risk Decision Banner */}
        <RiskDecisionBanner
          riskLevel={transaction.riskLevel}
          riskDecision={transaction.riskDecision}
          actionTaken={transaction.actionTaken}
          signals={transaction.signals}
          verifiedAt={transaction.verifiedAt}
        />

        <div className="divider" />

        {/* Merchant Info */}
        <div className="txn-detail-merchant">
          <h3 className="txn-detail-merchant-name">{transaction.merchantName}</h3>
          {transaction.merchantAddress && (
            <p className="txn-detail-merchant-address">{transaction.merchantAddress}</p>
          )}
        </div>

        {/* Statement descriptor */}
        {transaction.statementDescriptor && (
          <>
            <div className="divider" />
            <div className="txn-detail-statement">
              <p className="txn-detail-statement-label">Appears on your statement as:</p>
              <p className="txn-detail-statement-value">{transaction.statementDescriptor}</p>
              {transaction.cardAction && (
                <p className="txn-detail-statement-card">
                  Card {transaction.cardAction} on {formatDateFull(transaction.date)}
                </p>
              )}
            </div>
          </>
        )}

        <div className="divider" />

        {/* Actions */}
        <div className="txn-detail-actions">
          {transaction.merchantPhone && (
            <button className="txn-detail-action-row">
              <Phone size={20} />
              <span>Call {transaction.merchantPhone}</span>
            </button>
          )}
          {transaction.merchantWebsite && (
            <button className="txn-detail-action-row">
              <Globe size={20} />
              <span>Merchant Website</span>
            </button>
          )}
          <button className="txn-detail-action-row txn-detail-action-report">
            <AlertTriangle size={20} />
            <span>Report a Problem</span>
          </button>
        </div>
      </div>
    </div>
  )
}
