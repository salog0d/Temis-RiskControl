import { useState, useCallback } from 'react'
import { Lock, Info } from 'lucide-react'
import { useQuery } from '../../hooks/useQuery'
import { cardService } from '../../services/cardService'
import { PageHeader } from '../../components/layout/PageHeader'
import { Toggle } from '../../components/ui/Toggle'
import { Button } from '../../components/ui/Button'
import { PageSpinner } from '../../components/ui/Spinner'
import type { Card } from '../../types/card.types'
import './SecurityPage.css'

export function SecurityPage() {
  const { data: cards, loading, refetch } = useQuery<Card[]>(
    'cards',
    () => cardService.getCards()
  )
  const [toggling, setToggling] = useState<string | null>(null)

  const handleToggle = useCallback(async (cardId: string) => {
    setToggling(cardId)
    try {
      await cardService.toggleLock(cardId)
      await refetch()
    } finally {
      setToggling(null)
    }
  }, [refetch])

  if (loading) return <PageSpinner />

  return (
    <div className="security-page">
      <PageHeader title="Lock Card" />

      <div className="security-content">
        {/* Lock icon */}
        <div className="security-lock-icon">
          <Lock size={36} />
        </div>

        <p className="security-description">
          No one will be able to use this card, including you. You can turn it back on anytime.
        </p>

        {/* Card toggles */}
        <div className="security-card-list">
          {cards?.map(card => (
            <div key={card.id} className="security-card-row">
              <span className="security-card-name">
                {card.cardholderName}...{card.lastFour}
                {card.isLocked ? ' is locked' : ''}
              </span>
              <Toggle
                id={`lock-${card.id}`}
                checked={card.isLocked}
                onChange={() => handleToggle(card.id)}
                disabled={toggling === card.id}
              />
            </div>
          ))}
        </div>

        <Button variant="success" size="lg" fullWidth>
          Done
        </Button>

        <button className="security-learn-more">
          <Info size={16} />
          Learn more about Lock My Card
        </button>
      </div>
    </div>
  )
}
