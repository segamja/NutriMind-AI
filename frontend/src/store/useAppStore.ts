import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import type { CoachMessage, MealRecord, ScanResponse } from '../types'

interface AppState {
  darkMode: boolean
  toggleDarkMode: () => void
  lastScan: ScanResponse | null
  previewImage: string | null
  setLastScan: (scan: ScanResponse | null) => void
  setPreviewImage: (url: string | null) => void
  meals: MealRecord[]
  setMeals: (meals: MealRecord[]) => void
  addMeal: (meal: MealRecord) => void
  coachHistory: CoachMessage[]
  addCoachMessage: (msg: CoachMessage) => void
  clearCoachHistory: () => void
}

export const useAppStore = create<AppState>()(
  persist(
    (set) => ({
      darkMode: true,
      toggleDarkMode: () => set((s) => ({ darkMode: !s.darkMode })),
      lastScan: null,
      previewImage: null,
      setLastScan: (scan) => set({ lastScan: scan }),
      setPreviewImage: (url) => set({ previewImage: url }),
      meals: [],
      setMeals: (meals) => set({ meals }),
      addMeal: (meal) => set((s) => ({ meals: [meal, ...s.meals] })),
      coachHistory: [],
      addCoachMessage: (msg) =>
        set((s) => ({ coachHistory: [...s.coachHistory, msg] })),
      clearCoachHistory: () => set({ coachHistory: [] }),
    }),
    {
      name: 'nutrimind-storage',
      partialize: (state) => ({
        darkMode: state.darkMode,
        coachHistory: state.coachHistory,
      }),
    },
  ),
)
