import './Spinner.css'

interface SpinnerProps {
  size?: 'sm' | 'md' | 'lg'
}

export function Spinner({ size = 'md' }: SpinnerProps) {
  return (
    <div className={`spinner spinner-${size}`} role="status" aria-label="Loading">
      <span className="visually-hidden">Loading...</span>
    </div>
  )
}

export function PageSpinner() {
  return (
    <div className="page-spinner-container">
      <Spinner size="lg" />
    </div>
  )
}
