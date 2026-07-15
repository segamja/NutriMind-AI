import { useState, useRef, useEffect } from 'react'
import { Send, Bot, User, Trash2, Lightbulb } from 'lucide-react'
import { Card } from '../components/ui/Card'
import { Button } from '../components/ui/Button'
import { ErrorBanner } from '../components/ui/Loading'
import { chatWithCoach } from '../lib/api'
import { useAppStore } from '../store/useAppStore'
import type { CoachMessage } from '../types'

const QUICK_PROMPTS = [
  '오늘 치킨 먹어도 될까?',
  '단백질이 부족한가?',
  '오늘 저녁 추천해줘',
  '냉장고 재료로 만들 수 있는 음식은?',
]

export function CoachPage() {
  const { coachHistory, addCoachMessage, clearCoachHistory } = useAppStore()
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [lastActions, setLastActions] = useState<string[]>([])
  const [lastSuggestions, setLastSuggestions] = useState<string[]>([])
  const bottomRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [coachHistory])

  const sendMessage = async (text: string) => {
    if (!text.trim() || loading) return
    const userMsg: CoachMessage = { role: 'user', content: text.trim() }
    const updatedHistory = [...coachHistory, userMsg]
    addCoachMessage(userMsg)
    setInput('')
    setLoading(true)
    setError(null)

    try {
      const response = await chatWithCoach(text.trim(), updatedHistory)
      addCoachMessage({ role: 'assistant', content: response.reply })
      setLastActions(response.actions)
      setLastSuggestions(response.suggestions)
    } catch (e) {
      setError(e instanceof Error ? e.message : '응답을 받지 못했습니다.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex flex-col gap-4" style={{ minHeight: 'calc(100dvh - 180px)' }}>
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-gray-900 dark:text-white">AI Nutrition Coach</h2>
          <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
            영양 상담 및 식단 코칭
          </p>
        </div>
        {coachHistory.length > 0 && (
          <Button variant="ghost" size="sm" onClick={clearCoachHistory}>
            <Trash2 className="h-4 w-4" />
          </Button>
        )}
      </div>

      {error && <ErrorBanner message={error} onDismiss={() => setError(null)} />}

      <div className="flex-1 space-y-3 overflow-y-auto">
        {coachHistory.length === 0 && (
          <Card className="text-center">
            <Bot className="mx-auto h-10 w-10 text-emerald-500" />
            <p className="mt-2 text-sm text-gray-500 dark:text-gray-400">
              NutriMind AI 코치에게 무엇이든 물어보세요
            </p>
            <div className="mt-4 flex flex-wrap justify-center gap-2">
              {QUICK_PROMPTS.map((prompt) => (
                <button
                  key={prompt}
                  onClick={() => sendMessage(prompt)}
                  className="rounded-full bg-emerald-100 px-3 py-1.5 text-xs text-emerald-700 transition-colors hover:bg-emerald-200 dark:bg-emerald-900/30 dark:text-emerald-300 dark:hover:bg-emerald-900/50"
                >
                  {prompt}
                </button>
              ))}
            </div>
          </Card>
        )}

        {coachHistory.map((msg, i) => (
          <div
            key={i}
            className={`flex gap-2 ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}
          >
            <div
              className={`flex h-8 w-8 shrink-0 items-center justify-center rounded-full ${
                msg.role === 'user'
                  ? 'bg-emerald-500 text-white'
                  : 'bg-gray-200 text-gray-600 dark:bg-gray-700 dark:text-gray-300'
              }`}
            >
              {msg.role === 'user' ? (
                <User className="h-4 w-4" />
              ) : (
                <Bot className="h-4 w-4" />
              )}
            </div>
            <div
              className={`max-w-[80%] rounded-2xl px-4 py-2.5 text-sm ${
                msg.role === 'user'
                  ? 'bg-emerald-500 text-white'
                  : 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-200'
              }`}
            >
              {msg.content}
            </div>
          </div>
        ))}

        {loading && (
          <div className="flex gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-full bg-gray-200 dark:bg-gray-700">
              <Bot className="h-4 w-4 animate-pulse" />
            </div>
            <div className="rounded-2xl bg-gray-100 px-4 py-2.5 dark:bg-gray-800">
              <div className="flex gap-1">
                <span className="h-2 w-2 animate-bounce rounded-full bg-gray-400 [animation-delay:0ms]" />
                <span className="h-2 w-2 animate-bounce rounded-full bg-gray-400 [animation-delay:150ms]" />
                <span className="h-2 w-2 animate-bounce rounded-full bg-gray-400 [animation-delay:300ms]" />
              </div>
            </div>
          </div>
        )}

        {(lastActions.length > 0 || lastSuggestions.length > 0) && (
          <Card title="추천 행동" className="border-emerald-200 dark:border-emerald-800">
            {lastActions.map((action, i) => (
              <div key={i} className="flex items-start gap-2 text-sm text-gray-700 dark:text-gray-300">
                <Lightbulb className="mt-0.5 h-4 w-4 shrink-0 text-amber-500" />
                {action}
              </div>
            ))}
            {lastSuggestions.length > 0 && (
              <div className="mt-2 flex flex-wrap gap-2">
                {lastSuggestions.map((s) => (
                  <span
                    key={s}
                    className="rounded-full bg-emerald-100 px-3 py-1 text-xs text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-300"
                  >
                    {s}
                  </span>
                ))}
              </div>
            )}
          </Card>
        )}

        <div ref={bottomRef} />
      </div>

      <form
        onSubmit={(e) => {
          e.preventDefault()
          sendMessage(input)
        }}
        className="sticky bottom-20 flex gap-2"
      >
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="영양 관련 질문을 입력하세요..."
          className="flex-1 rounded-xl border border-gray-200 bg-white px-4 py-2.5 text-sm outline-none focus:border-emerald-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white"
          disabled={loading}
        />
        <Button type="submit" disabled={!input.trim() || loading}>
          <Send className="h-4 w-4" />
        </Button>
      </form>
    </div>
  )
}
