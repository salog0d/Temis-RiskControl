import { motion, AnimatePresence } from 'framer-motion'
import { ShieldAlert, Phone } from 'lucide-react'
import { Button } from '../ui/Button'
import './ActionBlockedOverlay.css'

interface ActionBlockedOverlayProps {
  isOpen: boolean
  onDismiss: () => void
  message?: string
}

export function ActionBlockedOverlay({ isOpen, onDismiss, message }: ActionBlockedOverlayProps) {
  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          className="blocked-overlay"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
        >
          <motion.div
            className="blocked-content"
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.9, opacity: 0 }}
            transition={{ type: 'spring', damping: 25, stiffness: 300 }}
          >
            <div className="blocked-icon-wrap">
              <ShieldAlert size={48} />
            </div>
            <h2 className="blocked-title">Action Blocked</h2>
            <p className="blocked-message">
              {message ?? 'This action was blocked for your security. We detected unusual activity on your account.'}
            </p>
            <div className="blocked-actions">
              <Button variant="secondary" fullWidth onClick={onDismiss}>
                Go Back
              </Button>
              <Button variant="ghost" fullWidth onClick={onDismiss}>
                <Phone size={16} />
                Contact Support
              </Button>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  )
}
