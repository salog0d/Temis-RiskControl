import { motion } from 'framer-motion'
import { useAuth } from '../../hooks/useAuth'
import { useQuery } from '../../hooks/useQuery'
import { accountService } from '../../services/accountService'
import { activityService } from '../../services/activityService'
import { GreetingBanner } from '../../components/shared/GreetingBanner'
import { AccountCard } from '../../components/shared/AccountCard'
import { ActivityEntry } from '../../components/fraud/ActivityEntry'
import { PageSpinner } from '../../components/ui/Spinner'
import type { Account } from '../../types/account.types'
import type { ActivityEvent } from '../../types/activity.types'
import './DashboardPage.css'

export function DashboardPage() {
  const { user } = useAuth()

  const { data: accounts, loading: accountsLoading } = useQuery<Account[]>(
    'accounts',
    () => accountService.getAccounts()
  )

  const { data: recentActivity } = useQuery<ActivityEvent[]>(
    'recent-activity',
    () => activityService.getActivity()
  )

  // Show pending items that need user action
  const pendingActions = recentActivity?.filter(e => !e.resolved) ?? []
  const latestActivity = recentActivity?.slice(0, 3) ?? []

  if (accountsLoading) return <PageSpinner />

  return (
    <div className="dashboard-page">
      <div className="dashboard-logo-container">
        <img src="/images/CapitalOne_Logo.png" alt="Capital One" className="dashboard-top-logo" />
      </div>
      <GreetingBanner name={user?.name ?? 'User'} />

      {/* Pending action banner */}
      {pendingActions.length > 0 && (
        <div className="dashboard-pending">
          <span className="dashboard-pending-dot" />
          <span>
            {pendingActions.length} action{pendingActions.length > 1 ? 's' : ''} require
            {pendingActions.length === 1 ? 's' : ''} your attention
          </span>
        </div>
      )}

      {/* Account cards */}
      <div className="dashboard-accounts">
        {accounts?.map((account, index) => (
          <motion.div
            key={account.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1, duration: 0.3 }}
          >
            <AccountCard account={account} />
          </motion.div>
        ))}
      </div>

      {/* Recent activity */}
      {latestActivity.length > 0 && (
        <div className="dashboard-section">
          <h2 className="section-title">Recent Activity</h2>
          <div className="dashboard-activity-list">
            {latestActivity.map(event => (
              <ActivityEntry key={event.id} event={event} />
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
