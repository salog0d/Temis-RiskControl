import type { ReactNode } from 'react'
import './Card.css'

interface CardProps {
  children: ReactNode
  variant?: 'default' | 'gradient'
  gradient?: string
  onClick?: () => void
  className?: string
}

export function Card({
  children,
  variant = 'default',
  gradient,
  onClick,
  className = '',
}: CardProps) {
  const style = gradient ? { background: gradient } : undefined
  const Tag = onClick ? 'button' : 'div'

  return (
    <Tag
      className={`card card-${variant} ${onClick ? 'card-interactive' : ''} ${className}`}
      style={style}
      onClick={onClick}
    >
      {children}
    </Tag>
  )
}

export function CardHeader({ children, className = '' }: { children: ReactNode; className?: string }) {
  return <div className={`card-header ${className}`}>{children}</div>
}

export function CardBody({ children, className = '' }: { children: ReactNode; className?: string }) {
  return <div className={`card-body ${className}`}>{children}</div>
}
