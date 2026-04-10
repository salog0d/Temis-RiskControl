/** Generic API response wrapper — matches FastAPI response model pattern */
export interface ApiResponse<T> {
  success: boolean
  data?: T
  error?: string
  message?: string
  meta?: {
    total: number
    page: number
    limit: number
  }
}

/** Generic paginated request params */
export interface PaginationParams {
  page?: number
  limit?: number
}
