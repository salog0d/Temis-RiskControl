import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from './context/AuthContext'
import { RiskProvider } from './context/RiskContext'
import { MobileShell } from './components/layout/MobileShell'
import { useAuth } from './hooks/useAuth'
import { LoginPage } from './pages/LoginPage/LoginPage'
import { DashboardPage } from './pages/DashboardPage/DashboardPage'
import { AccountDetailPage } from './pages/AccountDetailPage/AccountDetailPage'
import { TransactionDetailPage } from './pages/TransactionDetailPage/TransactionDetailPage'
import { SecurityPage } from './pages/SecurityPage/SecurityPage'
import { ActivityPage } from './pages/ActivityPage/ActivityPage'
import { SettingsPage } from './pages/SettingsPage/SettingsPage'
import { PageSpinner } from './components/ui/Spinner'
import type { ReactNode } from 'react'

/** Protects routes that require authentication */
function ProtectedRoute({ children }: { children: ReactNode }) {
  const { isAuthenticated, loading } = useAuth()

  if (loading) return <PageSpinner />
  if (!isAuthenticated) return <Navigate to="/login" replace />

  return <MobileShell>{children}</MobileShell>
}

function AppRoutes() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />

      <Route path="/dashboard" element={
        <ProtectedRoute><DashboardPage /></ProtectedRoute>
      } />
      <Route path="/accounts/:id" element={
        <ProtectedRoute><AccountDetailPage /></ProtectedRoute>
      } />
      <Route path="/transactions/:id" element={
        <ProtectedRoute><TransactionDetailPage /></ProtectedRoute>
      } />
      <Route path="/security" element={
        <ProtectedRoute><SecurityPage /></ProtectedRoute>
      } />
      <Route path="/activity" element={
        <ProtectedRoute><ActivityPage /></ProtectedRoute>
      } />
      <Route path="/settings" element={
        <ProtectedRoute><SettingsPage /></ProtectedRoute>
      } />

      {/* Default redirect */}
      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  )
}

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <RiskProvider>
          <AppRoutes />
        </RiskProvider>
      </AuthProvider>
    </BrowserRouter>
  )
}
