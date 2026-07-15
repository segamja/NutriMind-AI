import { useEffect, useState } from 'react'
import { Card } from '../components/ui/Card'
import { ErrorBanner } from '../components/ui/Loading'
import { getDashboardStats } from '../lib/api'
import { formatNumber } from '../lib/utils'
import type { DashboardStats } from '../types'

function SimpleBarChart({ data }: { data: { date: string; calories: number }[] }) {
  const maxCal = Math.max(...data.map((d) => d.calories), 1)

  return (
    <div className="flex h-48 items-end justify-between gap-1 pt-4">
      {data.map((item) => (
        <div key={item.date} className="flex flex-1 flex-col items-center gap-1">
          <span className="text-[10px] text-gray-500">
            {item.calories > 0 ? formatNumber(item.calories, 0) : ''}
          </span>
          <div
            className="w-full rounded-t-md bg-emerald-500 transition-all"
            style={{ height: `${Math.max((item.calories / maxCal) * 140, 4)}px` }}
          />
          <span className="text-[10px] text-gray-400">{item.date}</span>
        </div>
      ))}
    </div>
  )
}

export function DashboardPage() {
  const [stats, setStats] = useState<DashboardStats | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    getDashboardStats()
      .then(setStats)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false))
  }, [])

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="h-8 w-8 animate-spin-slow rounded-full border-4 border-emerald-500 border-t-transparent" />
      </div>
    )
  }

  if (error) {
    return <ErrorBanner message={error} />
  }

  if (!stats) return null

  const summaryCards = [
    { label: '오늘 칼로리', value: `${formatNumber(stats.today_calories)} kcal` },
    { label: '오늘 단백질', value: `${formatNumber(stats.today_protein, 1)} g` },
    { label: '평균 건강점수', value: `${formatNumber(stats.avg_health_score, 0)}점` },
    { label: '총 기록', value: `${stats.total_meals}회` },
  ]

  return (
    <div className="space-y-4">
      <div>
        <h2 className="text-xl font-bold text-gray-900 dark:text-white">Health Dashboard</h2>
        <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
          일간·주간 영양 통계
        </p>
      </div>

      <div className="grid grid-cols-2 gap-3">
        {summaryCards.map(({ label, value }) => (
          <Card key={label}>
            <p className="text-xs text-gray-500 dark:text-gray-400">{label}</p>
            <p className="mt-1 text-lg font-bold text-gray-900 dark:text-white">{value}</p>
          </Card>
        ))}
      </div>

      <Card title="주간 칼로리 추이">
        {stats.total_meals === 0 ? (
          <p className="py-8 text-center text-sm text-gray-500">
            아직 기록된 식사가 없습니다
          </p>
        ) : (
          <SimpleBarChart data={stats.weekly_calories} />
        )}
      </Card>

      <Card title="평균 영양 섭취">
        <div className="space-y-3">
          <div className="flex justify-between text-sm">
            <span className="text-gray-500">평균 칼로리</span>
            <span className="font-medium">{formatNumber(stats.avg_calories)} kcal</span>
          </div>
          <div className="flex justify-between text-sm">
            <span className="text-gray-500">평균 단백질</span>
            <span className="font-medium">{formatNumber(stats.avg_protein, 1)} g</span>
          </div>
        </div>
      </Card>
    </div>
  )
}
