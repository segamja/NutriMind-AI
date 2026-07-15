import { useCallback, useEffect, useState } from 'react'
import {
  applyUpdate,
  fetchRemoteVersion,
  isUpdateAvailable,
  type AppVersionInfo,
} from '../lib/version'

const CHECK_INTERVAL_MS = 5 * 60 * 1000

export function useVersionCheck() {
  const [updateAvailable, setUpdateAvailable] = useState<AppVersionInfo | null>(null)
  const [checking, setChecking] = useState(false)

  const checkForUpdate = useCallback(async () => {
    setChecking(true)
    try {
      const remote = await fetchRemoteVersion()
      if (isUpdateAvailable(remote)) {
        setUpdateAvailable(remote)
      }
    } catch {
      // Ignore transient network errors during background checks.
    } finally {
      setChecking(false)
    }
  }, [])

  useEffect(() => {
    if (import.meta.env.DEV) return

    void checkForUpdate()

    const intervalId = window.setInterval(() => {
      void checkForUpdate()
    }, CHECK_INTERVAL_MS)

    const onVisible = () => {
      if (document.visibilityState === 'visible') {
        void checkForUpdate()
      }
    }

    window.addEventListener('focus', checkForUpdate)
    document.addEventListener('visibilitychange', onVisible)

    return () => {
      window.clearInterval(intervalId)
      window.removeEventListener('focus', checkForUpdate)
      document.removeEventListener('visibilitychange', onVisible)
    }
  }, [checkForUpdate])

  const dismissUpdate = useCallback(() => {
    setUpdateAvailable(null)
  }, [])

  const confirmUpdate = useCallback(() => {
    applyUpdate(updateAvailable ?? undefined)
  }, [updateAvailable])

  return {
    updateAvailable,
    checking,
    checkForUpdate,
    dismissUpdate,
    confirmUpdate,
  }
}
