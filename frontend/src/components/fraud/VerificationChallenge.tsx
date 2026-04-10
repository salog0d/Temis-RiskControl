import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { ShieldCheck } from 'lucide-react'
import { Button } from '../ui/Button'
import { Input } from '../ui/Input'
import type { RiskResponse } from '../../types/risk.types'
import { verificationService } from '../../services/verificationService'
import './VerificationChallenge.css'

interface VerificationChallengeProps {
  isOpen: boolean
  riskResponse: RiskResponse | null
  onSuccess: () => void
  onDismiss: () => void
}

export function VerificationChallenge({
  isOpen,
  riskResponse,
  onSuccess,
  onDismiss,
}: VerificationChallengeProps) {
  const [code, setCode] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const actionTaken = riskResponse?.actionTaken ?? 'otp_sent'
  const verificationId = riskResponse?.verificationId ?? 'mock'

  const handleSubmit = async () => {
    setLoading(true)
    setError('')

    try {
      let success = false
      switch (actionTaken) {
        case 'otp_sent':
          success = await verificationService.submitOTP(verificationId, code)
          break
        case 'mfa_required':
          success = await verificationService.submitMFA(verificationId, code)
          break
        case 'password_required':
          success = await verificationService.submitPassword(verificationId, password)
          break
        default:
          success = true
      }

      if (success) {
        onSuccess()
        setCode('')
        setPassword('')
      } else {
        setError('Verification failed. Please try again.')
      }
    } catch {
      setError('An error occurred. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const renderContent = () => {
    switch (actionTaken) {
      case 'otp_sent':
        return (
          <>
            <p className="challenge-subtitle">Enter the code we sent to your phone</p>
            <Input
              id="otp-input"
              type="text"
              inputMode="numeric"
              maxLength={6}
              placeholder="000000"
              value={code}
              onChange={e => setCode(e.target.value.replace(/\D/g, ''))}
              error={error}
              autoFocus
            />
          </>
        )
      case 'mfa_required':
        return (
          <>
            <p className="challenge-subtitle">Enter the code from your authenticator app</p>
            <Input
              id="mfa-input"
              type="text"
              inputMode="numeric"
              maxLength={6}
              placeholder="000000"
              value={code}
              onChange={e => setCode(e.target.value.replace(/\D/g, ''))}
              error={error}
              autoFocus
            />
          </>
        )
      case 'password_required':
        return (
          <>
            <p className="challenge-subtitle">Re-enter your password to continue</p>
            <Input
              id="password-input"
              type="password"
              placeholder="Password"
              value={password}
              onChange={e => setPassword(e.target.value)}
              error={error}
              autoFocus
            />
          </>
        )
      default:
        return <p className="challenge-subtitle">Additional verification is required</p>
    }
  }

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          className="challenge-overlay"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
        >
          <motion.div
            className="challenge-content"
            initial={{ y: 50, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            exit={{ y: 50, opacity: 0 }}
            transition={{ type: 'spring', damping: 25, stiffness: 300 }}
          >
            <div className="challenge-icon-wrap">
              <ShieldCheck size={40} />
            </div>
            <h2 className="challenge-title">Verify Your Identity</h2>
            {renderContent()}
            <div className="challenge-actions">
              <Button
                variant="primary"
                fullWidth
                onClick={handleSubmit}
                loading={loading}
                disabled={
                  (actionTaken === 'password_required' && !password) ||
                  (actionTaken !== 'password_required' && code.length < 6)
                }
              >
                Verify
              </Button>
              <Button variant="ghost" fullWidth onClick={onDismiss}>
                Cancel
              </Button>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  )
}
