import type {
  CoachMessage,
  CoachResponse,
  DashboardStats,
  MealRecord,
  ScanResponse,
  VisionAnalysis,
  WeeklyReport,
} from '../types'

const API_BASE = import.meta.env.VITE_API_URL || '/api'

function formatApiError(detail: unknown): string {
  if (typeof detail === 'string') return detail
  if (Array.isArray(detail)) {
    return detail
      .map((item) => {
        if (typeof item === 'string') return item
        if (item && typeof item === 'object' && 'msg' in item) {
          return String((item as { msg: string }).msg)
        }
        return JSON.stringify(item)
      })
      .join(', ')
  }
  if (detail && typeof detail === 'object') {
    return JSON.stringify(detail)
  }
  return 'Request failed'
}

async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }))
    throw new Error(formatApiError(err.detail))
  }
  return res.json()
}

export async function scanFood(image: File): Promise<ScanResponse> {
  const form = new FormData()
  const filename = image.name || 'food.jpg'
  form.append('image', image, filename.endsWith('.') ? 'food.jpg' : filename)
  const controller = new AbortController()
  const timeout = setTimeout(() => controller.abort(), 120_000)
  try {
    const res = await fetch(`${API_BASE}/scan`, {
      method: 'POST',
      body: form,
      signal: controller.signal,
    })
    return handleResponse<ScanResponse>(res)
  } catch (e) {
    if (e instanceof DOMException && e.name === 'AbortError') {
      throw new Error('분석 시간이 초과되었습니다. 잠시 후 다시 시도하세요.')
    }
    throw e
  } finally {
    clearTimeout(timeout)
  }
}

export async function saveMeal(data: {
  food_name: string
  image_url?: string
  nutrition: VisionAnalysis['nutrition']
  health_score: number
  ingredients: string[]
  actions: string[]
}): Promise<MealRecord> {
  const res = await fetch(`${API_BASE}/meals`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })
  return handleResponse<MealRecord>(res)
}

export async function getMeals(): Promise<MealRecord[]> {
  const res = await fetch(`${API_BASE}/meals`)
  return handleResponse<MealRecord[]>(res)
}

export async function getTodayMeals(): Promise<MealRecord[]> {
  const res = await fetch(`${API_BASE}/meals/today`)
  return handleResponse<MealRecord[]>(res)
}

export async function chatWithCoach(
  message: string,
  history: CoachMessage[],
): Promise<CoachResponse> {
  const res = await fetch(`${API_BASE}/coach`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, history }),
  })
  return handleResponse<CoachResponse>(res)
}

export async function getDashboardStats(): Promise<DashboardStats> {
  const res = await fetch(`${API_BASE}/dashboard/stats`)
  return handleResponse<DashboardStats>(res)
}

export async function getWeeklyReport(): Promise<WeeklyReport> {
  const res = await fetch(`${API_BASE}/reports/weekly`)
  return handleResponse<WeeklyReport>(res)
}

export async function checkHealth(): Promise<{ openai_configured: boolean }> {
  const res = await fetch(`${API_BASE}/health`)
  return handleResponse(res)
}
