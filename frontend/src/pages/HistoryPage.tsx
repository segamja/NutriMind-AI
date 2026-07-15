import { useEffect, useState } from 'react'
import { Clock, Flame } from 'lucide-react'
import { Card } from '../components/ui/Card'
import { ErrorBanner } from '../components/ui/Loading'
import { getMeals } from '../lib/api'
import { useAppStore } from '../store/useAppStore'
import { formatNumber, getScoreColor } from '../lib/utils'

export function HistoryPage() {
  const { meals, setMeals } = useAppStore()
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    getMeals()
      .then(setMeals)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false))
  }, [setMeals])

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="h-8 w-8 animate-spin-slow rounded-full border-4 border-emerald-500 border-t-transparent" />
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <div>
        <h2 className="text-xl font-bold text-gray-900 dark:text-white">식사 기록</h2>
        <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
          {meals.length}개의 기록
        </p>
      </div>

      {error && <ErrorBanner message={error} />}

      {meals.length === 0 ? (
        <Card className="py-12 text-center">
          <p className="text-gray-500 dark:text-gray-400">
            아직 기록된 식사가 없습니다
          </p>
          <p className="mt-1 text-sm text-gray-400">
            음식을 스캔하고 기록을 저장해보세요
          </p>
        </Card>
      ) : (
        <div className="space-y-3">
          {meals.map((meal) => (
            <Card key={meal.id} className="flex gap-3">
              {meal.image_url ? (
                <img
                  src={meal.image_url}
                  alt={meal.food_name}
                  className="h-20 w-20 shrink-0 rounded-xl object-cover"
                />
              ) : (
                <div className="flex h-20 w-20 shrink-0 items-center justify-center rounded-xl bg-gray-100 dark:bg-gray-700">
                  <Flame className="h-8 w-8 text-emerald-500" />
                </div>
              )}
              <div className="min-w-0 flex-1">
                <div className="flex items-start justify-between gap-2">
                  <h3 className="truncate font-semibold text-gray-900 dark:text-white">
                    {meal.food_name}
                  </h3>
                  <span className={`shrink-0 text-sm font-bold ${getScoreColor(meal.health_score)}`}>
                    {meal.health_score}점
                  </span>
                </div>
                <p className="mt-1 text-sm text-gray-500">
                  {formatNumber(meal.nutrition.calories)} kcal · 단백질{' '}
                  {formatNumber(meal.nutrition.protein, 1)}g
                </p>
                <div className="mt-1.5 flex items-center gap-1 text-xs text-gray-400">
                  <Clock className="h-3 w-3" />
                  {new Date(meal.created_at).toLocaleString('ko-KR')}
                </div>
                {meal.actions.length > 0 && (
                  <p className="mt-1 truncate text-xs text-emerald-600 dark:text-emerald-400">
                    💡 {meal.actions[0]}
                  </p>
                )}
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  )
}
