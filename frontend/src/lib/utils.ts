import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatNumber(n: number, decimals = 0): string {
  return n.toFixed(decimals)
}

export function getScoreColor(score: number): string {
  if (score >= 80) return 'text-emerald-500'
  if (score >= 60) return 'text-amber-500'
  return 'text-red-500'
}

export function getScoreBg(score: number): string {
  if (score >= 80) return 'bg-emerald-500'
  if (score >= 60) return 'bg-amber-500'
  return 'bg-red-500'
}

const IMAGE_EXTENSIONS = /\.(jpe?g|png|webp|gif|heic|heif|bmp|avif)$/i

export function isLikelyImageFile(file: File): boolean {
  if (file.type.startsWith('image/')) return true
  if (!file.type || file.type === 'application/octet-stream') {
    return IMAGE_EXTENSIONS.test(file.name)
  }
  return false
}
