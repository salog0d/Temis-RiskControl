import { useLocation, useNavigate } from 'react-router-dom'
import { Home, CreditCard, Shield, Activity, MoreHorizontal } from 'lucide-react'
import './BottomTabBar.css'

const TABS = [
  { path: '/dashboard', icon: Home, label: 'Home' },
  { path: '/accounts/acc_001', icon: CreditCard, label: 'Accounts' },
  { path: '/security', icon: Shield, label: 'Security' },
  { path: '/activity', icon: Activity, label: 'Activity' },
  { path: '/settings', icon: MoreHorizontal, label: 'More' },
] as const

export function BottomTabBar() {
  const location = useLocation()
  const navigate = useNavigate()

  const isActive = (path: string) => {
    if (path === '/dashboard') return location.pathname === '/dashboard'
    return location.pathname.startsWith(path.split('/').slice(0, 2).join('/'))
  }

  return (
    <nav className="bottom-tab-bar" aria-label="Main navigation">
      {TABS.map(tab => {
        const active = isActive(tab.path)
        const Icon = tab.icon
        return (
          <button
            key={tab.path}
            className={`tab-item ${active ? 'tab-active' : ''}`}
            onClick={() => navigate(tab.path)}
            aria-current={active ? 'page' : undefined}
          >
            <Icon size={22} strokeWidth={active ? 2.5 : 1.8} />
            <span className="tab-label">{tab.label}</span>
          </button>
        )
      })}
    </nav>
  )
}
