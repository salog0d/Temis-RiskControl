import { useState } from 'react'
import { ChevronDown, ChevronUp } from 'lucide-react'
import type { Signal } from '../../types/transaction.types'
import './SignalSummary.css'

interface SignalSummaryProps {
  signals: Signal[]
}

export function SignalSummary({ signals }: SignalSummaryProps) {
  const [expanded, setExpanded] = useState(false)

  if (signals.length === 0) return null

  return (
    <div className="signal-summary">
      <button
        className="signal-summary-toggle"
        onClick={() => setExpanded(prev => !prev)}
      >
        <span>Why was this flagged?</span>
        {expanded ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
      </button>
      {expanded && (
        <ul className="signal-list">
          {signals.map((signal, index) => (
            <li key={index} className="signal-item">
              <span className={`signal-dot signal-dot-${signal.severity ?? 'low'}`} />
              <span>{signal.label}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
