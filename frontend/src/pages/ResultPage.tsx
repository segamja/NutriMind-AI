import { useNavigate } from 'react-router-dom'
import { CheckCircle, ArrowRight, Save, RotateCcw } from 'lucide-react'
import { Card } from '../components/ui/Card'
import { Button } from '../components/ui/Button'
import { ScoreRing } from '../components/ui/ScoreRing'
import { ErrorBanner } from '../components/ui/Loading'
import { useAppStore } from '../store/useAppStore'
import { saveMeal } from '../lib/api'
import { formatNumber } from '../lib/utils'
import { useState } from 'react'

export function ResultPage() {
  const navigate = useNavigate()
  const { lastScan, previewImage, addMeal } = useAppStore()
  const [saving, setSaving] = useState(false)
  const [saved, setSaved] = useState(false)
  const [error, setError] = useState<string | null>(null)

  if (!lastScan) {
    return (
      <div className="flex flex-col items-center gap-4 py-12">
        <p className="text-gray-500">분석 결과가 없습니다.</p>
        <Button onClick={() => navigate('/camera')}>음식 스캔하기</Button>
      </div>
    )
  }

  const { cnn, vision } = lastScan
  const { nutrition, health_score } = vision

  const handleSave = async () => {
    setSaving(true)
    setError(null)
    try {
      const meal = await saveMeal({
        food_name: vision.food_name,
        image_url: previewImage ?? undefined,
        nutrition,
        health_score: health_score.overall,
        ingredients: vision.ingredients,
        actions: vision.actions,
      })
      addMeal(meal)
      setSaved(true)
    } catch (e) {
      setError(e instanceof Error ? e.message : '저장에 실패했습니다.')
    } finally {
      setSaving(false)
    }
  }

  const nutrients = [
    { label: '칼로리', value: `${formatNumber(nutrition.calories)} kcal`, score: health_score.calories },
    { label: '단백질', value: `${formatNumber(nutrition.protein, 1)} g`, score: health_score.protein },
    { label: '지방', value: `${formatNumber(nutrition.fat, 1)} g`, score: health_score.fat },
    { label: '탄수화물', value: `${formatNumber(nutrition.carbohydrates, 1)} g`, score: health_score.carbohydrates },
    { label: '식이섬유', value: `${formatNumber(nutrition.fiber, 1)} g`, score: health_score.fiber },
    { label: '당류', value: `${formatNumber(nutrition.sugar, 1)} g`, score: health_score.sugar },
    { label: '나트륨', value: `${formatNumber(nutrition.sodium, 0)} mg`, score: health_score.sodium },
  ]

  return (
    <div className="space-y-4">
      {error && <ErrorBanner message={error} onDismiss={() => setError(null)} />}

      {previewImage && (
        <img
          src={previewImage}
          alt={vision.food_name}
          className="aspect-video w-full rounded-2xl object-cover"
        />
      )}

      <Card>
        <div className="flex items-start justify-between gap-4">
          <div>
            <h2 className="text-xl font-bold text-gray-900 dark:text-white">
              {vision.food_name}
            </h2>
            <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
              {vision.description}
            </p>
            <p className="mt-2 text-xs text-gray-400">
              CNN: {cnn.food_name} ({(cnn.confidence * 100).toFixed(0)}%) · {vision.cooking_method}
            </p>
          </div>
          <ScoreRing score={health_score.overall} size={80} />
        </div>
      </Card>

      <Card title="재료" subtitle={`${vision.ingredients.length}개 감지`}>
        <div className="flex flex-wrap gap-2">
          {vision.ingredients.map((ing) => (
            <span
              key={ing}
              className="rounded-full bg-emerald-100 px-3 py-1 text-sm text-emerald-700 dark:bg-emerald-900/40 dark:text-emerald-300"
            >
              {ing}
            </span>
          ))}
        </div>
      </Card>

      <Card title="양 추정 (Portion)">
        <div className="space-y-2">
          {vision.portions.map((p) => (
            <div
              key={p.name}
              className="flex items-center justify-between text-sm"
            >
              <span className="text-gray-700 dark:text-gray-300">{p.name}</span>
              <span className="font-medium text-gray-900 dark:text-white">
                {formatNumber(p.amount_g, 0)}g
                <span className="ml-1 text-xs text-gray-400">
                  ({(p.confidence * 100).toFixed(0)}%)
                </span>
              </span>
            </div>
          ))}
        </div>
      </Card>

      <Card title="영양소 분석">
        <div className="grid grid-cols-2 gap-3">
          {nutrients.map(({ label, value, score }) => (
            <div
              key={label}
              className="rounded-xl bg-gray-50 p-3 dark:bg-gray-900/50"
            >
              <p className="text-xs text-gray-500 dark:text-gray-400">{label}</p>
              <p className="mt-0.5 font-semibold text-gray-900 dark:text-white">{value}</p>
              <div className="mt-1.5 h-1 overflow-hidden rounded-full bg-gray-200 dark:bg-gray-700">
                <div
                  className="h-full rounded-full bg-emerald-500"
                  style={{ width: `${score}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      </Card>

      <Card title="AI 코칭 — 다음 행동" subtitle="Action Recommendations">
        <ul className="space-y-2">
          {vision.actions.map((action, i) => (
            <li
              key={i}
              className="flex items-start gap-2 text-sm text-gray-700 dark:text-gray-300"
            >
              <ArrowRight className="mt-0.5 h-4 w-4 shrink-0 text-emerald-500" />
              {action}
            </li>
          ))}
        </ul>
      </Card>

      <div className="grid grid-cols-2 gap-3 pb-4">
        <Button variant="secondary" onClick={() => navigate('/camera')}>
          <RotateCcw className="h-4 w-4" />
          다시 스캔
        </Button>
        <Button
          onClick={handleSave}
          loading={saving}
          disabled={saved}
        >
          {saved ? (
            <>
              <CheckCircle className="h-4 w-4" />
              저장됨
            </>
          ) : (
            <>
              <Save className="h-4 w-4" />
              식사 기록
            </>
          )}
        </Button>
      </div>
    </div>
  )
}
