import { useNavigate } from 'react-router-dom'
import { ArrowLeft } from 'lucide-react'
import './PageHeader.css'

interface PageHeaderProps {
  title: string
  showBack?: boolean
  rightAction?: React.ReactNode
}

export function PageHeader({ title, showBack = false, rightAction }: PageHeaderProps) {
  const navigate = useNavigate()

  return (
    <header className="page-header">
      <div className="page-header-left">
        {showBack && (
          <button className="page-header-back" onClick={() => navigate(-1)} aria-label="Go back">
            <ArrowLeft size={22} />
          </button>
        )}
      </div>
      <h1 className="page-header-title">{title}</h1>
      <div className="page-header-right">
        {rightAction}
      </div>
    </header>
  )
}
