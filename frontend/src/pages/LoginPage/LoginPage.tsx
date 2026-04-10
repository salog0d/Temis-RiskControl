import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Shield } from 'lucide-react'
import { useAuth } from '../../hooks/useAuth'
import { Button } from '../../components/ui/Button'
import { Input } from '../../components/ui/Input'
import './LoginPage.css'

export function LoginPage() {
  const navigate = useNavigate()
  const { login } = useAuth()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!email.trim() || !password.trim()) {
      setError('Please enter your email and password')
      return
    }

    setLoading(true)
    setError('')

    const success = await login(email, password)
    if (success) {
      navigate('/dashboard', { replace: true })
    } else {
      setError('Invalid credentials. Please try again.')
    }
    setLoading(false)
  }

  return (
    <div className="login-page">
      <div className="login-header">
        <div className="login-logo">
          <Shield size={40} strokeWidth={1.5} />
        </div>
        <h1 className="login-brand">Temis</h1>
        <p className="login-tagline">Secure Banking</p>
      </div>

      <form className="login-form" onSubmit={handleSubmit}>
        <Input
          id="login-email"
          type="email"
          label="Email"
          placeholder="you@example.com"
          value={email}
          onChange={e => setEmail(e.target.value)}
          autoComplete="email"
        />
        <Input
          id="login-password"
          type="password"
          label="Password"
          placeholder="Password"
          value={password}
          onChange={e => setPassword(e.target.value)}
          error={error}
          autoComplete="current-password"
        />
        <Button
          type="submit"
          variant="primary"
          size="lg"
          fullWidth
          loading={loading}
        >
          Sign In
        </Button>
        <button type="button" className="login-forgot">
          Forgot password?
        </button>
      </form>
    </div>
  )
}
