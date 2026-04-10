import { useParams } from 'react-router-dom'
import { useQuery } from '../../hooks/useQuery'
import { accountService } from '../../services/accountService'
import { PageHeader } from '../../components/layout/PageHeader'
import { Card } from '../../components/ui/Card'
import { PageSpinner } from '../../components/ui/Spinner'
import { TransactionRow } from '../../components/shared/TransactionRow'
import { splitCurrency } from '../../utils/formatCurrency'
import { formatDateFull } from '../../utils/formatDate'
import { ACCOUNT_GRADIENTS } from '../../utils/constants'
import type { Account } from '../../types/account.types'
import type { Transaction } from '../../types/transaction.types'
import './AccountDetailPage.css'

export function AccountDetailPage() {
  const { id } = useParams<{ id: string }>()

  const { data: account, loading: accountLoading } = useQuery<Account | undefined>(
    `account-${id}`,
    () => accountService.getAccountById(id!)
  )

  const { data: transactions, loading: txnLoading } = useQuery<Transaction[]>(
    `account-txns-${id}`,
    () => accountService.getAccountTransactions(id!)
  )

  if (accountLoading || txnLoading) return <PageSpinner />
  if (!account) return <div className="page">Account not found</div>

  const gradient = ACCOUNT_GRADIENTS[account.type] ?? ACCOUNT_GRADIENTS.checking
  const { whole, cents } = splitCurrency(account.balance, account.currency)

  // Group transactions by date
  const grouped = new Map<string, Transaction[]>()
  for (const txn of (transactions ?? [])) {
    const label = formatDateFull(txn.date)
    const existing = grouped.get(label) ?? []
    grouped.set(label, [...existing, txn])
  }

  return (
    <div className="account-detail-page">
      <PageHeader title={account.name} showBack />

      <Card variant="gradient" gradient={gradient} className="account-detail-header">
        <div className="account-detail-header-inner">
          <p className="account-detail-name">{account.name}...{account.lastFour}</p>
          <p className="account-detail-balance">
            {whole}<sup className="account-detail-cents">{cents}</sup>
          </p>
          <p className="account-detail-label">Current balance</p>
        </div>
      </Card>

      <div className="account-detail-transactions">
        <h2 className="section-title" style={{ padding: '0 var(--space-4)' }}>Transactions</h2>
        {Array.from(grouped.entries()).map(([dateLabel, txns]) => (
          <div key={dateLabel} className="txn-date-group">
            <h3 className="txn-date-label">{dateLabel}</h3>
            <div className="txn-date-list">
              {txns.map(txn => (
                <TransactionRow key={txn.id} transaction={txn} />
              ))}
            </div>
          </div>
        ))}
        {(transactions?.length ?? 0) === 0 && (
          <p className="account-detail-empty">No transactions yet</p>
        )}
      </div>
    </div>
  )
}
