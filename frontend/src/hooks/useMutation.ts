import { useState, useCallback } from 'react'

/**
 * Generic mutation hook for POST/PATCH/DELETE operations.
 */
export function useMutation<TData, TVariables>(
  mutationFn: (variables: TVariables) => Promise<TData>
) {
  const [data, setData] = useState<TData | null>(null)
  const [error, setError] = useState<Error | null>(null)
  const [loading, setLoading] = useState(false)

  const mutate = useCallback(async (variables: TVariables): Promise<TData | null> => {
    setLoading(true)
    setError(null)

    try {
      const result = await mutationFn(variables)
      setData(result)
      return result
    } catch (err) {
      const mutationError = err as Error
      setError(mutationError)
      return null
    } finally {
      setLoading(false)
    }
  }, [mutationFn])

  return { mutate, data, error, loading }
}
