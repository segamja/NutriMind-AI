import { cn, getScoreBg, getScoreColor } from '../../lib/utils'

interface ScoreRingProps {
  score: number
  size?: number
  label?: string
}

export function ScoreRing({ score, size = 96, label = 'Health Score' }: ScoreRingProps) {
  const radius = (size - 12) / 2
  const circumference = 2 * Math.PI * radius
  const offset = circumference - (score / 100) * circumference

  return (
    <div className="flex flex-col items-center gap-2">
      <div className="relative" style={{ width: size, height: size }}>
        <svg width={size} height={size} className="-rotate-90">
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            fill="none"
            stroke="currentColor"
            strokeWidth={8}
            className="text-gray-200 dark:text-gray-700"
          />
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            fill="none"
            stroke="currentColor"
            strokeWidth={8}
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            strokeLinecap="round"
            className={getScoreColor(score)}
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className={cn('text-2xl font-bold', getScoreColor(score))}>
            {score}
          </span>
          <span className="text-xs text-gray-500 dark:text-gray-400">/ 100</span>
        </div>
      </div>
      <span className="text-sm font-medium text-gray-600 dark:text-gray-300">
        {label}
      </span>
      <div className={cn('h-1.5 w-16 rounded-full', getScoreBg(score))} />
    </div>
  )
}
