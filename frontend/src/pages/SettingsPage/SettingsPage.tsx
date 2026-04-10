import { User, Bell, Shield, ChevronRight, LogOut } from 'lucide-react'
import { useAuth } from '../../hooks/useAuth'
import { useNavigate } from 'react-router-dom'
import { PageHeader } from '../../components/layout/PageHeader'
import './SettingsPage.css'

export function SettingsPage() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = async () => {
    await logout()
    navigate('/login', { replace: true })
  }

  return (
    <div className="settings-page">
      <PageHeader title="Settings" />

      {/* Profile section */}
      <div className="settings-profile">
        <div className="settings-avatar">
          <User size={28} />
        </div>
        <div className="settings-profile-info">
          <p className="settings-profile-name">{user?.name ?? 'User'}</p>
          <p className="settings-profile-email">{user?.email ?? ''}</p>
        </div>
      </div>

      {/* Setting groups */}
      <div className="settings-group">
        <h3 className="section-title" style={{ padding: '0 var(--space-4)' }}>Notifications</h3>
        <div className="settings-list">
          <button className="settings-row">
            <Bell size={20} />
            <span className="settings-row-label">Push Notifications</span>
            <ChevronRight size={18} className="settings-row-chevron" />
          </button>
        </div>
      </div>

      <div className="settings-group">
        <h3 className="section-title" style={{ padding: '0 var(--space-4)' }}>Security</h3>
        <div className="settings-list">
          <button className="settings-row">
            <Shield size={20} />
            <span className="settings-row-label">Change Password</span>
            <ChevronRight size={18} className="settings-row-chevron" />
          </button>
          <button className="settings-row">
            <Shield size={20} />
            <span className="settings-row-label">Two-Factor Authentication</span>
            <ChevronRight size={18} className="settings-row-chevron" />
          </button>
        </div>
      </div>

      <div className="settings-group">
        <div className="settings-list">
          <button className="settings-row settings-row-danger" onClick={handleLogout}>
            <LogOut size={20} />
            <span className="settings-row-label">Sign Out</span>
          </button>
        </div>
      </div>

      <p className="settings-version">Temis RiskControl v0.1.0</p>
    </div>
  )
}
