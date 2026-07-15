import { cn } from '../../lib/utils'

interface LoadingOverlayProps {
  message?: string
}

export function LoadingOverlay({ message = 'AI 분석 중...' }: LoadingOverlayProps) {
  return (
    <div className="fixed inset-0 z-50 flex flex-col items-center justify-center bg-black/60 backdrop-blur-sm">
      <div className="animate-scan rounded-full border-4 border-emerald-400 p-6">
        <div className="h-12 w-12 animate-spin-slow rounded-full border-4 border-emerald-500 border-t-transparent" />
      </div>
      <p className="mt-6 text-lg font-medium text-white">{message}</p>
      <p className="mt-2 text-sm text-gray-300">CNN 인식 → Vision 분석 → 영양 계산</p>
    </div>
  )
}

interface ErrorBannerProps {
  message: string
  onDismiss?: () => void
}

export function ErrorBanner({ message, onDismiss }: ErrorBannerProps) {
  return (
    <div
      className={cn(
        'rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700',
        'dark:border-red-800 dark:bg-red-950 dark:text-red-300',
      )}
    >
      <div className="flex items-start justify-between gap-2">
        <p>{message}</p>
        {onDismiss && (
          <button
            onClick={onDismiss}
            className="shrink-0 text-red-500 hover:text-red-700"
          >
            ✕
          </button>
        )}
      </div>
    </div>
  )
}
