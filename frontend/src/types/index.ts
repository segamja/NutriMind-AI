export interface NutritionInfo {
  calories: number
  protein: number
  fat: number
  carbohydrates: number
  fiber: number
  sugar: number
  sodium: number
  calcium: number
  iron: number
  potassium: number
}

export interface MealScore {
  overall: number
  calories: number
  protein: number
  fat: number
  carbohydrates: number
  sugar: number
  sodium: number
  fiber: number
}

export interface PortionItem {
  name: string
  amount_g: number
  confidence: number
}

export interface CNNResult {
  food_name: string
  confidence: number
  category: string
}

export interface VisionAnalysis {
  food_name: string
  description: string
  ingredients: string[]
  cooking_method: string
  portions: PortionItem[]
  nutrition: NutritionInfo
  health_score: MealScore
  actions: string[]
}

export interface ScanResponse {
  cnn: CNNResult
  vision: VisionAnalysis
  scan_id?: string
}

export interface MealRecord {
  id: string
  food_name: string
  image_url?: string
  nutrition: NutritionInfo
  health_score: number
  ingredients: string[]
  actions: string[]
  created_at: string
}

export interface CoachMessage {
  role: 'user' | 'assistant'
  content: string
}

export interface CoachResponse {
  reply: string
  actions: string[]
  suggestions: string[]
}

export interface DashboardStats {
  total_meals: number
  avg_calories: number
  avg_protein: number
  avg_health_score: number
  today_calories: number
  today_protein: number
  weekly_calories: { date: string; calories: number }[]
}
