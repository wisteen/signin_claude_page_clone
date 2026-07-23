import { existsSync } from 'node:fs'
import { spawnSync } from 'node:child_process'
import { resolve } from 'node:path'

const projectRoot = resolve(import.meta.dirname, '..')
const npmCommand = process.platform === 'win32' ? 'npm.cmd' : 'npm'
const npxCommand = process.platform === 'win32' ? 'npx.cmd' : 'npx'
const playwrightPath = resolve(projectRoot, 'node_modules', 'playwright')

function run(command, args) {
  const isWindowsCommand = command.endsWith('.cmd')
  const result = spawnSync(
    isWindowsCommand ? 'cmd.exe' : command,
    isWindowsCommand ? ['/d', '/s', '/c', command, ...args] : args,
    {
    cwd: projectRoot,
    stdio: 'inherit',
    shell: false
    }
  )

  if (result.status !== 0) {
    if (result.error) {
      console.error(result.error.message)
    }
    process.exit(result.status || 1)
  }
}

if (!existsSync(playwrightPath)) {
  console.log('Playwright package is missing. Running npm install...')
  run(npmCommand, ['install'])
}

console.log('Checking Playwright Chromium browser...')
run(npxCommand, ['playwright', 'install', 'chromium'])
