import type { ReactNode } from 'react'
import { BottomTabBar } from './BottomTabBar'
import './MobileShell.css'

interface MobileShellProps {
  children: ReactNode
}

export function MobileShell({ children }: MobileShellProps) {
  return (
    <div className="mobile-shell">
      <main className="mobile-shell-content">
        {children}
      </main>
      <BottomTabBar />
    </div>
  )
}
