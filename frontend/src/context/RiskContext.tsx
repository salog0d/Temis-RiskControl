import { createContext, useContext, useState, useCallback, type ReactNode } from 'react'
import type { RiskResponse } from '../types/risk.types'

interface RiskContextValue {
  /** Currently active verification challenge, if any */
  activeChallenge: RiskResponse | null
  showChallenge: boolean
  showBlocked: boolean
  presentChallenge: (response: RiskResponse) => void
  presentBlocked: (response: RiskResponse) => void
  dismissAll: () => void
}

const RiskContext = createContext<RiskContextValue | undefined>(undefined)

export function RiskProvider({ children }: { children: ReactNode }) {
  const [activeChallenge, setActiveChallenge] = useState<RiskResponse | null>(null)
  const [showChallenge, setShowChallenge] = useState(false)
  const [showBlocked, setShowBlocked] = useState(false)

  const presentChallenge = useCallback((response: RiskResponse) => {
    setActiveChallenge(response)
    setShowChallenge(true)
  }, [])

  const presentBlocked = useCallback((response: RiskResponse) => {
    setActiveChallenge(response)
    setShowBlocked(true)
  }, [])

  const dismissAll = useCallback(() => {
    setShowChallenge(false)
    setShowBlocked(false)
    setActiveChallenge(null)
  }, [])

  return (
    <RiskContext.Provider value={{
      activeChallenge,
      showChallenge,
      showBlocked,
      presentChallenge,
      presentBlocked,
      dismissAll,
    }}>
      {children}
    </RiskContext.Provider>
  )
}

export function useRisk() {
  const context = useContext(RiskContext)
  if (!context) throw new Error('useRisk must be used within RiskProvider')
  return context
}
