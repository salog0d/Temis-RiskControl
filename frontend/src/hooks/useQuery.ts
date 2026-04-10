import { useState, useEffect, useCallback, useRef } from 'react'

interface UseQueryOptions<T> {
  onSuccess?: (data: T) => void
  onError?: (error: Error) => void
  enabled?: boolean
}

/**
 * Generic async data-fetching hook.
 * Follows the frontend-patterns skill's useQuery pattern.
 */
export function useQuery<T>(
  key: string,
  fetcher: () => Promise<T>,
  options?: UseQueryOptions<T>
) {
  const [data, setData] = useState<T | null>(null)
  const [error, setError] = useState<Error | null>(null)
  const [loading, setLoading] = useState(false)
  const fetcherRef = useRef(fetcher)
  fetcherRef.current = fetcher

  const refetch = useCallback(async () => {
    setLoading(true)
    setError(null)

    try {
      const result = await fetcherRef.current()
      setData(result)
      options?.onSuccess?.(result)
    } catch (err) {
      const fetchError = err as Error
      setError(fetchError)
      options?.onError?.(fetchError)
    } finally {
      setLoading(false)
    }
  // Intentionally only depend on key to avoid infinite loops
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [key])

  useEffect(() => {
    if (options?.enabled !== false) {
      refetch()
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [key, refetch])

  return { data, error, loading, refetch }
}
