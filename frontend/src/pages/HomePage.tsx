import { useNavigate } from 'react-router-dom'
import { Camera, Sparkles, TrendingUp, Apple } from 'lucide-react'
import { Card } from '../components/ui/Card'
import { Button } from '../components/ui/Button'
import { useAppStore } from '../store/useAppStore'
import { formatNumber } from '../lib/utils'

export function HomePage() {
  const navigate = useNavigate()
  const { meals } = useAppStore()

  const todayCalories = meals
    .filter((m) => {
      const today = new Date().toDateString()
      return new Date(m.created_at).toDateString() === today
    })
    .reduce((sum, m) => sum + m.nutrition.calories, 0)

  const features = [
    {
      icon: Camera,
      title: 'AI Food Scanner',
      desc: '사진 한 장으로 음식과 영양소를 분석합니다',
    },
    {
      icon: Sparkles,
      title: 'AI Nutrition Coach',
      desc: '맞춤형 식단 코칭과 행동 제안을 받으세요',
    },
    {
      icon: TrendingUp,
      title: 'Health Dashboard',
      desc: '일간·주간 영양 통계를 한눈에 확인하세요',
    },
  ]

  return (
    <div className="space-y-6">
      <section className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-emerald-500 to-teal-600 p-6 text-white">
        <div className="relative z-10">
          <p className="text-sm font-medium text-emerald-100">오늘의 영양</p>
          <p className="mt-1 text-3xl font-bold">
            {formatNumber(todayCalories)} <span className="text-lg">kcal</span>
          </p>
          <p className="mt-2 text-sm text-emerald-100">
            {meals.length > 0
              ? `${meals.length}개의 식사 기록`
              : '첫 식사를 기록해보세요!'}
          </p>
          <Button
            className="mt-4 bg-white text-emerald-600 hover:bg-emerald-50"
            onClick={() => navigate('/camera')}
          >
            <Camera className="h-4 w-4" />
            음식 스캔하기
          </Button>
        </div>
        <Apple className="absolute -bottom-4 -right-4 h-32 w-32 text-white/10" />
      </section>

      <section className="grid gap-3">
        {features.map(({ icon: Icon, title, desc }) => (
          <Card key={title} className="flex items-start gap-3">
            <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-emerald-100 dark:bg-emerald-900/30">
              <Icon className="h-5 w-5 text-emerald-600 dark:text-emerald-400" />
            </div>
            <div>
              <h3 className="font-semibold text-gray-900 dark:text-white">{title}</h3>
              <p className="mt-0.5 text-sm text-gray-500 dark:text-gray-400">{desc}</p>
            </div>
          </Card>
        ))}
      </section>

      <Card title="빠른 시작">
        <div className="grid grid-cols-2 gap-2">
          <Button variant="secondary" onClick={() => navigate('/coach')}>
            AI 코치에게 질문
          </Button>
          <Button variant="secondary" onClick={() => navigate('/history')}>
            식사 기록 보기
          </Button>
        </div>
      </Card>
    </div>
  )
}
