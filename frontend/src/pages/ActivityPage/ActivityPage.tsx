import { useState, useCallback } from 'react'
import { useQuery } from '../../hooks/useQuery'
import { activityService } from '../../services/activityService'
import { PageHeader } from '../../components/layout/PageHeader'
import { ActivityEntry } from '../../components/fraud/ActivityEntry'
import { BottomSheet } from '../../components/ui/BottomSheet'
import { Badge } from '../../components/ui/Badge'
import { PageSpinner } from '../../components/ui/Spinner'
import { SignalSummary } from '../../components/fraud/SignalSummary'
import { formatDateTimeShort } from '../../utils/formatDate'
import { getRiskDisplay } from '../../utils/riskLevel'
import type { ActivityEvent } from '../../types/activity.types'
import './ActivityPage.css'

const FILTER_TABS = [
  { key: 'all', label: 'All' },
  { key: 'blocked', label: 'Blocked' },
  { key: 'verified', label: 'Verified' },
  { key: 'requires_action', label: 'Action Needed' },
]

export function ActivityPage() {
  const [activeFilter, setActiveFilter] = useState('all')
  const [selectedEvent, setSelectedEvent] = useState<ActivityEvent | null>(null)

  const { data: events, loading } = useQuery<ActivityEvent[]>(
    `activity-${activeFilter}`,
    () => activityService.getActivity(activeFilter)
  )

  const handleSelectEvent = useCallback((event: ActivityEvent) => {
    setSelectedEvent(event)
  }, [])

  if (loading) return <PageSpinner />

  return (
    <div className="activity-page">
      <PageHeader title="Activity & Alerts" />

      {/* Filter tabs */}
      <div className="activity-filters">
        {FILTER_TABS.map(tab => (
          <button
            key={tab.key}
            className={`activity-filter-tab ${activeFilter === tab.key ? 'activity-filter-active' : ''}`}
            onClick={() => setActiveFilter(tab.key)}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Event list */}
      <div className="activity-list">
        {events?.map(event => (
          <ActivityEntry
            key={event.id}
            event={event}
            onClick={() => handleSelectEvent(event)}
          />
        ))}
        {(events?.length ?? 0) === 0 && (
          <p className="activity-empty">No activity to show</p>
        )}
      </div>

      {/* Detail bottom sheet */}
      <BottomSheet
        isOpen={!!selectedEvent}
        onClose={() => setSelectedEvent(null)}
        title="Event Details"
      >
        {selectedEvent && <ActivityDetailContent event={selectedEvent} />}
      </BottomSheet>
    </div>
  )
}

function ActivityDetailContent({ event }: { event: ActivityEvent }) {
  const display = getRiskDisplay(event.riskLevel)
  const badgeVariant = event.riskLevel === 'high' ? 'danger'
    : event.riskLevel === 'medium' ? 'warning'
    : 'success'

  return (
    <div className="activity-detail">
      <div className="activity-detail-row">
        <span className="activity-detail-label">When</span>
        <span>{formatDateTimeShort(event.timestamp)}</span>
      </div>
      <div className="activity-detail-row">
        <span className="activity-detail-label">Trigger</span>
        <span>{event.triggerDescription}</span>
      </div>
      <div className="activity-detail-row">
        <span className="activity-detail-label">Risk Level</span>
        <Badge variant={badgeVariant} size="md">
          {display.icon} {display.label}
        </Badge>
      </div>
      <div className="activity-detail-row">
        <span className="activity-detail-label">Decision</span>
        <span>{event.actionLabel}</span>
      </div>
      <div className="activity-detail-row">
        <span className="activity-detail-label">Status</span>
        <Badge variant={event.resolved ? 'success' : 'warning'} size="md">
          {event.resolved ? 'Resolved' : 'Pending'}
        </Badge>
      </div>
      {event.signals && event.signals.length > 0 && (
        <div className="activity-detail-signals">
          <SignalSummary signals={event.signals} />
        </div>
      )}
    </div>
  )
}
