import type { ActivityEvent } from '../types/activity.types'
import { MOCK_ACTIVITY } from '../mocks/activity.mock'
import { MOCK_API_DELAY_MS } from '../utils/constants'

export const activityService = {
  async getActivity(filter?: string): Promise<ActivityEvent[]> {
    await new Promise(resolve => setTimeout(resolve, MOCK_API_DELAY_MS))

    if (!filter || filter === 'all') return MOCK_ACTIVITY

    return MOCK_ACTIVITY.filter(event => {
      switch (filter) {
        case 'blocked': return event.decision === 'blocked'
        case 'verified': return event.decision === 'step_up_required' && event.resolved
        case 'requires_action': return !event.resolved
        default: return true
      }
    })
  },

  async getActivityById(id: string): Promise<ActivityEvent | undefined> {
    await new Promise(resolve => setTimeout(resolve, MOCK_API_DELAY_MS / 2))
    return MOCK_ACTIVITY.find(e => e.id === id)
  },
}
