import { readFileSync, writeFileSync } from 'node:fs'
import { dirname, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..')
const pkg = JSON.parse(readFileSync(resolve(root, 'package.json'), 'utf-8'))
const payload = {
  version: pkg.version,
  build: new Date().toISOString(),
}

writeFileSync(resolve(root, 'public/version.json'), `${JSON.stringify(payload, null, 2)}\n`)

console.log(`version.json → v${payload.version} (${payload.build})`)
