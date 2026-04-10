import { useNavigate } from 'react-router-dom'
import { Card } from '../ui/Card'
import { splitCurrency } from '../../utils/formatCurrency'
import { ACCOUNT_GRADIENTS } from '../../utils/constants'
import type { Account } from '../../types/account.types'
import './AccountCard.css'

interface AccountCardProps {
  account: Account
}

export function AccountCard({ account }: AccountCardProps) {
  const navigate = useNavigate()
  const gradient = ACCOUNT_GRADIENTS[account.type] ?? ACCOUNT_GRADIENTS.checking
  const { whole, cents } = splitCurrency(account.balance, account.currency)

  return (
    <Card
      variant="gradient"
      gradient={gradient}
      onClick={() => navigate(`/accounts/${account.id}`)}
      className="account-card"
    >
      <div className="account-card-inner">
        <p className="account-card-name">
          {account.name}...{account.lastFour}
        </p>
        <p className="account-card-balance">
          {whole}<sup className="account-card-cents">{cents}</sup>
        </p>
        <p className="account-card-label">Current balance</p>
      </div>
    </Card>
  )
}
