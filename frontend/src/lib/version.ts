export interface AppVersionInfo {
  version: string
  build: string
}

export const APP_VERSION = __APP_VERSION__
export const APP_BUILD = __APP_BUILD__

export function formatVersionLabel(version = APP_VERSION): string {
  return `v${version}`
}

export async function fetchRemoteVersion(): Promise<AppVersionInfo> {
  const res = await fetch(`/version.json?_=${Date.now()}`, {
    cache: 'no-store',
  })
  if (!res.ok) {
    throw new Error('Failed to fetch version')
  }
  return res.json() as Promise<AppVersionInfo>
}

export function isUpdateAvailable(remote: AppVersionInfo): boolean {
  return remote.version !== APP_VERSION || remote.build !== APP_BUILD
}

export function applyUpdate(remote?: AppVersionInfo): void {
  const url = new URL(window.location.href)
  url.searchParams.set('_v', remote?.version ?? String(Date.now()))
  window.location.replace(url.toString())
}
