/**
 * Returns a time-of-day aware greeting.
 * Matches Capital One's "Good morning, Elly" pattern.
 */
export function getGreetingText(name: string): string {
  const hour = new Date().getHours()

  if (hour < 12) return `Good morning, ${name}`
  if (hour < 17) return `Good afternoon, ${name}`
  return `Good evening, ${name}`
}
