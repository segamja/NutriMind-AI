import { RefreshCw, Sparkles } from 'lucide-react'
import { Button } from './ui/Button'
import { APP_BUILD, APP_VERSION, formatUpdateLabel } from '../lib/version'
import type { AppVersionInfo } from '../lib/version'

interface UpdatePromptProps {
  remote: AppVersionInfo
  onUpdate: () => void
  onDismiss: () => void
}

export function UpdatePrompt({ remote, onUpdate, onDismiss }: UpdatePromptProps) {
  return (
    <div className="fixed inset-0 z-[60] flex items-end justify-center bg-black/50 p-4 backdrop-blur-sm sm:items-center">
      <div
        role="dialog"
        aria-labelledby="update-title"
        aria-describedby="update-desc"
        className="w-full max-w-sm rounded-2xl border border-emerald-200 bg-white p-5 shadow-xl dark:border-emerald-800 dark:bg-gray-900"
      >
        <div className="flex items-start gap-3">
          <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-emerald-100 dark:bg-emerald-900/40">
            <Sparkles className="h-5 w-5 text-emerald-600 dark:text-emerald-400" />
          </div>
          <div>
            <h2 id="update-title" className="text-base font-semibold text-gray-900 dark:text-white">
              새 버전이 있습니다
            </h2>
            <p id="update-desc" className="mt-1 text-sm text-gray-600 dark:text-gray-300">
              {formatUpdateLabel(APP_VERSION, APP_BUILD, remote)}
              <br />
              업데이트하면 최신 기능과 수정 사항이 적용됩니다.
            </p>
          </div>
        </div>

        <div className="mt-5 flex gap-2">
          <Button variant="secondary" className="flex-1" onClick={onDismiss}>
            나중에
          </Button>
          <Button className="flex-1" onClick={onUpdate}>
            <RefreshCw className="h-4 w-4" />
            업데이트
          </Button>
        </div>
      </div>
    </div>
  )
}
