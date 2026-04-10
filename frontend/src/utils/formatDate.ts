const DEFAULT_LOCALE = 'en-US'

/** "Monday, June 3" */
export function formatDateFull(dateString: string): string {
  return new Date(dateString).toLocaleDateString(DEFAULT_LOCALE, {
    weekday: 'long',
    month: 'long',
    day: 'numeric',
  })
}

/** "Jun 3" */
export function formatDateShort(dateString: string): string {
  return new Date(dateString).toLocaleDateString(DEFAULT_LOCALE, {
    month: 'short',
    day: 'numeric',
  })
}

/** "Jun 3, 2:14 PM" */
export function formatDateTimeShort(dateString: string): string {
  return new Date(dateString).toLocaleDateString(DEFAULT_LOCALE, {
    month: 'short',
    day: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
  })
}

/** "2:14 PM" */
export function formatTime(dateString: string): string {
  return new Date(dateString).toLocaleTimeString(DEFAULT_LOCALE, {
    hour: 'numeric',
    minute: '2-digit',
  })
}

/** Groups items by date label, e.g. "Monday, June 3" */
export function groupByDate<T extends { date: string }>(
  items: T[]
): Map<string, T[]> {
  const groups = new Map<string, T[]>()

  for (const item of items) {
    const label = formatDateFull(item.date)
    const existing = groups.get(label) ?? []
    groups.set(label, [...existing, item])
  }

  return groups
}
