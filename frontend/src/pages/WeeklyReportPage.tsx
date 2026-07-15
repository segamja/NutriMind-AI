import { useEffect, useState } from 'react'
import { FileText, Target, TrendingUp, Lightbulb } from 'lucide-react'
import { Card } from '../components/ui/Card'
import { Button } from '../components/ui/Button'
import { ErrorBanner } from '../components/ui/Loading'
import { ScoreRing } from '../components/ui/ScoreRing'
import { getWeeklyReport } from '../lib/api'
import type { WeeklyReport } from '../types'

export function WeeklyReportPage() {
  const [report, setReport] = useState<WeeklyReport | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const loadReport = async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await getWeeklyReport()
      setReport(data)
    } catch (e) {
      setReport(null)
      setError(e instanceof Error ? e.message : '리포트 생성에 실패했습니다.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadReport()
  }, [])

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center gap-3 py-20">
        <div className="h-8 w-8 animate-spin-slow rounded-full border-4 border-emerald-500 border-t-transparent" />
        <p className="text-sm text-gray-500">AI가 주간 리포트를 생성 중...</p>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <div className="flex items-start justify-between gap-3">
        <div>
          <h2 className="text-xl font-bold text-gray-900 dark:text-white">Weekly AI Report</h2>
          <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
            OpenAI Responses API 기반 주간 건강 분석
          </p>
        </div>
        <Button variant="secondary" size="sm" onClick={loadReport}>
          새로고침
        </Button>
      </div>

      {error && <ErrorBanner message={error} onDismiss={() => setError(null)} />}

      {report && (
        <>
          <Card className="bg-gradient-to-br from-emerald-50 to-teal-50 dark:from-emerald-950/30 dark:to-teal-950/30">
            <div className="flex items-start justify-between gap-4">
              <div>
                <p className="text-sm text-emerald-600 dark:text-emerald-400">{report.period}</p>
                <p className="mt-2 text-lg font-semibold text-gray-900 dark:text-white">
                  {report.summary}
                </p>
                <p className="mt-1 text-sm text-gray-500">
                  {report.total_meals}회 식사 기록 분석
                </p>
              </div>
              <ScoreRing score={Math.round(report.avg_health_score)} size={72} label="주간 점수" />
            </div>
          </Card>

          <Card title="식습관 분석" subtitle="Habit Analysis">
            <div className="flex gap-3">
              <TrendingUp className="mt-0.5 h-5 w-5 shrink-0 text-emerald-500" />
              <p className="text-sm leading-relaxed text-gray-700 dark:text-gray-300">
                {report.habit_analysis}
              </p>
            </div>
          </Card>

          <Card title="영양소 분석" subtitle="Nutrient Analysis">
            <div className="flex gap-3">
              <FileText className="mt-0.5 h-5 w-5 shrink-0 text-emerald-500" />
              <p className="text-sm leading-relaxed text-gray-700 dark:text-gray-300">
                {report.nutrient_analysis}
              </p>
            </div>
          </Card>

          <Card title="개선사항">
            <ul className="space-y-2">
              {report.improvements.map((item, i) => (
                <li key={i} className="flex items-start gap-2 text-sm text-gray-700 dark:text-gray-300">
                  <Lightbulb className="mt-0.5 h-4 w-4 shrink-0 text-amber-500" />
                  {item}
                </li>
              ))}
            </ul>
          </Card>

          <Card title="다음 주 목표">
            <ul className="space-y-2">
              {report.next_week_goals.map((goal, i) => (
                <li key={i} className="flex items-start gap-2 text-sm text-gray-700 dark:text-gray-300">
                  <Target className="mt-0.5 h-4 w-4 shrink-0 text-emerald-500" />
                  {goal}
                </li>
              ))}
            </ul>
          </Card>
        </>
      )}
    </div>
  )
}
