import { getRiskDisplay } from '../../utils/riskLevel'
import { formatDateTimeShort } from '../../utils/formatDate'
import type { ActivityEvent } from '../../types/activity.types'
import './ActivityEntry.css'

interface ActivityEntryProps {
  event: ActivityEvent
  onClick?: () => void
}

export function ActivityEntry({ event, onClick }: ActivityEntryProps) {
  const display = getRiskDisplay(event.riskLevel)

  return (
    <button className="activity-entry" onClick={onClick}>
      <span
        className="activity-entry-bar"
        style={{ backgroundColor: display.color }}
      />
      <div className="activity-entry-content">
        <div className="activity-entry-header">
          <span className="activity-entry-icon">{display.icon}</span>
          <span className="activity-entry-time">
            {formatDateTimeShort(event.timestamp)}
          </span>
        </div>
        <p className="activity-entry-desc">{event.triggerDescription}</p>
        <p className="activity-entry-action">{event.actionLabel}</p>
        {!event.resolved && (
          <span className="activity-entry-pending">Requires action</span>
        )}
      </div>
    </button>
  )
}
