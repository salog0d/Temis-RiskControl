const DEFAULT_CURRENCY = 'USD'
const DEFAULT_LOCALE = 'en-US'

/**
 * Formats a number as currency.
 *
 * @param amount - The numeric amount
 * @param currency - ISO 4217 currency code (default: USD)
 * @returns Formatted string like "$1,093.07"
 */
export function formatCurrency(
  amount: number,
  currency: string = DEFAULT_CURRENCY
): string {
  return new Intl.NumberFormat(DEFAULT_LOCALE, {
    style: 'currency',
    currency,
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(amount)
}

/**
 * Splits a formatted currency string into dollars and cents for
 * the superscript-cents display style used in Capital One UI.
 *
 * @returns { whole: "$1,093", cents: "07" }
 */
export function splitCurrency(
  amount: number,
  currency: string = DEFAULT_CURRENCY
): { whole: string; cents: string } {
  const formatted = formatCurrency(amount, currency)
  const parts = formatted.split('.')
  return {
    whole: parts[0],
    cents: parts[1] ?? '00',
  }
}
