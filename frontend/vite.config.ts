import { defineConfig, type Plugin } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import { readFileSync, writeFileSync } from 'node:fs'
import { dirname, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const root = resolve(dirname(fileURLToPath(import.meta.url)))

interface VersionInfo {
  version: string
  build: string
}

function createVersionInfo(): VersionInfo {
  const pkg = JSON.parse(readFileSync(resolve(root, 'package.json'), 'utf-8'))
  return {
    version: pkg.version,
    build: process.env.VERCEL_GIT_COMMIT_SHA ?? new Date().toISOString(),
  }
}

function persistVersionJson(info: VersionInfo) {
  writeFileSync(resolve(root, 'public/version.json'), `${JSON.stringify(info, null, 2)}\n`)
}

let versionInfo = createVersionInfo()
persistVersionJson(versionInfo)

function versionPlugin(): Plugin {
  return {
    name: 'version-json',
    configureServer() {
      versionInfo = createVersionInfo()
      persistVersionJson(versionInfo)
    },
    buildStart() {
      versionInfo = createVersionInfo()
      persistVersionJson(versionInfo)
    },
  }
}

export default defineConfig({
  define: {
    __APP_VERSION__: JSON.stringify(versionInfo.version),
    __APP_BUILD__: JSON.stringify(versionInfo.build),
  },
  plugins: [versionPlugin(), react(), tailwindcss()],
  server: {
    host: true,
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8800',
        changeOrigin: true,
        timeout: 120_000,
      },
    },
  },
})
