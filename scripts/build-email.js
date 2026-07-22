import { mkdir, readFile, writeFile } from 'node:fs/promises'
import { dirname, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const allowedHosts = new Set([
  'localhost',
  '127.0.0.1',
  '[::1]',
  '::1',
  'lab.local'
])

function parseArgs(argv) {
  const args = {}

  for (let index = 0; index < argv.length; index += 1) {
    const item = argv[index]
    if (!item.startsWith('--')) {
      continue
    }

    const key = item.slice(2)
    const value = argv[index + 1]

    if (!value || value.startsWith('--')) {
      throw new Error(`Missing value for --${key}`)
    }

    args[key] = value
    index += 1
  }

  return args
}

function escapeHtml(value) {
  return value
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#39;')
}

function validateLink(value) {
  let url

  try {
    url = new URL(value)
  } catch {
    throw new Error('Link must be a valid absolute URL.')
  }

  if (!['http:', 'https:'].includes(url.protocol)) {
    throw new Error('Link must use http or https.')
  }

  if (!allowedHosts.has(url.hostname)) {
    throw new Error(`Link host "${url.hostname}" is not allowed. Use localhost, 127.0.0.1, ::1, or lab.local.`)
  }

  return url.toString()
}

async function main() {
  const args = parseArgs(process.argv.slice(2))
  const name = args.name?.trim()
  const link = args.link?.trim()
  const out = args.out?.trim()

  if (!name || !link || !out) {
    throw new Error('Usage: npm run build-email -- --name "Alex" --link "http://localhost:5173" --out out/email.html')
  }

  const safeName = escapeHtml(name)
  const safeLink = escapeHtml(validateLink(link))
  const projectRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..')
  const templatePath = resolve(projectRoot, 'email', 'template.html')
  const outputPath = resolve(projectRoot, out)

  const template = await readFile(templatePath, 'utf8')
  const rendered = template
    .replaceAll('{{name}}', safeName)
    .replaceAll('{{link}}', safeLink)

  await mkdir(dirname(outputPath), { recursive: true })
  await writeFile(outputPath, rendered, 'utf8')
  console.log(`Built email: ${outputPath}`)
}

main().catch((error) => {
  console.error(`Email build failed: ${error.message}`)
  process.exit(1)
})
