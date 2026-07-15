import type {
  CoachMessage,
  CoachResponse,
  DashboardStats,
  MealRecord,
  ScanResponse,
  VisionAnalysis,
} from '../types'

const API_BASE = '/api'

async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }))
    throw new Error(err.detail || 'Request failed')
  }
  return res.json()
}

export async function scanFood(image: File): Promise<ScanResponse> {
  const form = new FormData()
  form.append('image', image)
  const res = await fetch(`${API_BASE}/scan`, { method: 'POST', body: form })
  return handleResponse<ScanResponse>(res)
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

export async function checkHealth(): Promise<{ openai_configured: boolean }> {
  const res = await fetch(`${API_BASE}/health`)
  return handleResponse(res)
}
