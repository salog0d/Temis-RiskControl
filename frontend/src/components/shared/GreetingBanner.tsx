import { getGreetingText } from '../../utils/greetingText'
import './GreetingBanner.css'

interface GreetingBannerProps {
  name: string
}

export function GreetingBanner({ name }: GreetingBannerProps) {
  const greeting = getGreetingText(name)

  return (
    <div className="greeting-banner">
      <h1 className="greeting-text">{greeting}</h1>
    </div>
  )
}
