import { useRef, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Camera, Upload, ImageIcon } from 'lucide-react'
import { Card } from '../components/ui/Card'
import { Button } from '../components/ui/Button'
import { LoadingOverlay, ErrorBanner } from '../components/ui/Loading'
import { scanFood } from '../lib/api'
import { useAppStore } from '../store/useAppStore'

export function CameraPage() {
  const navigate = useNavigate()
  const fileInputRef = useRef<HTMLInputElement>(null)
  const cameraInputRef = useRef<HTMLInputElement>(null)
  const [preview, setPreview] = useState<string | null>(null)
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const { setLastScan, setPreviewImage } = useAppStore()

  const handleFile = (file: File) => {
    if (!file.type.startsWith('image/')) {
      setError('이미지 파일만 업로드할 수 있습니다.')
      return
    }
    setSelectedFile(file)
    setPreview(URL.createObjectURL(file))
    setError(null)
  }

  const handleAnalyze = async () => {
    if (!selectedFile) return
    setLoading(true)
    setError(null)
    try {
      const result = await scanFood(selectedFile)
      setLastScan(result)
      setPreviewImage(preview)
      navigate('/result')
    } catch (e) {
      setError(e instanceof Error ? e.message : '분석에 실패했습니다.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-4">
      <div>
        <h2 className="text-xl font-bold text-gray-900 dark:text-white">AI Food Scanner</h2>
        <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
          음식 사진을 촬영하거나 업로드하세요
        </p>
      </div>

      {error && <ErrorBanner message={error} onDismiss={() => setError(null)} />}

      <Card className="overflow-hidden p-0">
        {preview ? (
          <img src={preview} alt="Preview" className="aspect-square w-full object-cover" />
        ) : (
          <div className="flex aspect-square flex-col items-center justify-center gap-4 bg-gray-100 dark:bg-gray-800">
            <div className="animate-scan rounded-full border-4 border-dashed border-emerald-300 p-8 dark:border-emerald-700">
              <Camera className="h-12 w-12 text-emerald-500" />
            </div>
            <p className="text-sm text-gray-500 dark:text-gray-400">
              사진을 촬영하거나 갤러리에서 선택하세요
            </p>
          </div>
        )}
      </Card>

      <div className="grid grid-cols-2 gap-3">
        <Button
          variant="secondary"
          onClick={() => cameraInputRef.current?.click()}
        >
          <Camera className="h-4 w-4" />
          카메라
        </Button>
        <Button
          variant="secondary"
          onClick={() => fileInputRef.current?.click()}
        >
          <Upload className="h-4 w-4" />
          갤러리
        </Button>
      </div>

      <input
        ref={cameraInputRef}
        type="file"
        accept="image/*"
        capture="environment"
        className="hidden"
        onChange={(e) => e.target.files?.[0] && handleFile(e.target.files[0])}
      />
      <input
        ref={fileInputRef}
        type="file"
        accept="image/*"
        className="hidden"
        onChange={(e) => e.target.files?.[0] && handleFile(e.target.files[0])}
      />

      <Button
        className="w-full"
        size="lg"
        disabled={!selectedFile}
        loading={loading}
        onClick={handleAnalyze}
      >
        <ImageIcon className="h-5 w-5" />
        AI 분석 시작
      </Button>

      <Card title="분석 파이프라인" subtitle="TECH_SPEC Phase 1 MVP">
        <ol className="space-y-2 text-sm text-gray-600 dark:text-gray-300">
          <li className="flex items-center gap-2">
            <span className="flex h-6 w-6 items-center justify-center rounded-full bg-emerald-100 text-xs font-bold text-emerald-700 dark:bg-emerald-900 dark:text-emerald-300">1</span>
            CNN 음식 인식 (Mock)
          </li>
          <li className="flex items-center gap-2">
            <span className="flex h-6 w-6 items-center justify-center rounded-full bg-emerald-100 text-xs font-bold text-emerald-700 dark:bg-emerald-900 dark:text-emerald-300">2</span>
            OpenAI Vision 분석
          </li>
          <li className="flex items-center gap-2">
            <span className="flex h-6 w-6 items-center justify-center rounded-full bg-emerald-100 text-xs font-bold text-emerald-700 dark:bg-emerald-900 dark:text-emerald-300">3</span>
            영양소 계산 & 건강 점수
          </li>
        </ol>
      </Card>

      {loading && <LoadingOverlay />}
    </div>
  )
}
