import { NavLink, Outlet } from 'react-router-dom'
import {
  Camera,
  Home,
  MessageCircle,
  BarChart3,
  History,
  Moon,
  Sun,
  Leaf,
  FileText,
} from 'lucide-react'
import { UpdatePrompt } from './UpdatePrompt'
import { useVersionCheck } from '../hooks/useVersionCheck'
import { useAppStore } from '../store/useAppStore'
import { cn } from '../lib/utils'
import { formatDisplayVersion } from '../lib/version'

const navItems = [
  { to: '/', icon: Home, label: '홈' },
  { to: '/camera', icon: Camera, label: '스캔' },
  { to: '/dashboard', icon: BarChart3, label: '대시보드' },
  { to: '/report', icon: FileText, label: '리포트' },
  { to: '/history', icon: History, label: '기록' },
  { to: '/coach', icon: MessageCircle, label: '코치' },
]

export function Layout() {
  const { darkMode, toggleDarkMode } = useAppStore()
  const { updateAvailable, dismissUpdate, confirmUpdate } = useVersionCheck()

  return (
    <div className={cn('min-h-dvh bg-gray-50 dark:bg-gray-950', darkMode && 'dark')}>
      <header className="sticky top-0 z-40 border-b border-gray-200 bg-white/80 backdrop-blur-md dark:border-gray-800 dark:bg-gray-900/80">
        <div className="mx-auto flex max-w-lg items-center justify-between px-4 py-3">
          <div className="flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-emerald-500">
              <Leaf className="h-5 w-5 text-white" />
            </div>
            <div>
              <h1 className="text-lg font-bold text-gray-900 dark:text-white">
                NutriMind AI
              </h1>
              <p className="text-xs text-emerald-600 dark:text-emerald-400">
                Snap. Analyze. Improve. · {formatDisplayVersion()}
              </p>
            </div>
          </div>
          <button
            onClick={toggleDarkMode}
            className="rounded-lg p-2 text-gray-600 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-800"
            aria-label="Toggle dark mode"
          >
            {darkMode ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
          </button>
        </div>
      </header>

      <main className="mx-auto max-w-lg px-4 pb-24 pt-4">
        <Outlet />
      </main>

      <p className="pointer-events-none fixed bottom-[4.5rem] left-0 right-0 z-30 text-center text-[10px] text-gray-400 dark:text-gray-600">
        NutriMind AI {formatDisplayVersion()}
      </p>

      {updateAvailable && (
        <UpdatePrompt
          remote={updateAvailable}
          onUpdate={confirmUpdate}
          onDismiss={dismissUpdate}
        />
      )}

      <nav className="fixed bottom-0 left-0 right-0 z-40 border-t border-gray-200 bg-white/90 backdrop-blur-md dark:border-gray-800 dark:bg-gray-900/90">
        <div className="mx-auto flex max-w-lg items-center justify-around px-2 py-2">
          {navItems.map(({ to, icon: Icon, label }) => (
            <NavLink
              key={to}
              to={to}
              end={to === '/'}
              className={({ isActive }) =>
                cn(
                  'flex flex-col items-center gap-0.5 rounded-xl px-3 py-1.5 text-xs transition-colors',
                  isActive
                    ? 'text-emerald-600 dark:text-emerald-400'
                    : 'text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200',
                )
              }
            >
              <Icon className="h-5 w-5" />
              <span>{label}</span>
            </NavLink>
          ))}
        </div>
      </nav>
    </div>
  )
}
