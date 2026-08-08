import { createReadStream, statSync } from 'node:fs'
import { createServer } from 'node:http'
import { dirname, extname, resolve, sep } from 'node:path'
import { fileURLToPath } from 'node:url'

const directory = dirname(fileURLToPath(import.meta.url))
const publicDirectory = resolve(directory, 'dist')
const port = Number.parseInt(process.env.PORT || '4173', 10)

const contentTypes = {
  '.css': 'text/css; charset=utf-8',
  '.html': 'text/html; charset=utf-8',
  '.ico': 'image/x-icon',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.js': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.png': 'image/png',
  '.svg': 'image/svg+xml',
  '.webp': 'image/webp',
  '.woff': 'font/woff',
  '.woff2': 'font/woff2',
}

const securityHeaders = {
  'Content-Security-Policy': [
    "default-src 'self'",
    "base-uri 'self'",
    "object-src 'none'",
    "frame-ancestors 'none'",
    "form-action 'self'",
    "img-src 'self' data:",
    "font-src 'self' https://fonts.gstatic.com",
    "style-src 'self' https://fonts.googleapis.com",
    "style-src-attr 'unsafe-inline'",
    "script-src 'self'",
    "connect-src 'self'",
    'upgrade-insecure-requests',
  ].join('; '),
  'Cross-Origin-Opener-Policy': 'same-origin',
  'Cross-Origin-Resource-Policy': 'same-origin',
  'Permissions-Policy': 'camera=(), microphone=(), geolocation=(), payment=()',
  'Referrer-Policy': 'strict-origin-when-cross-origin',
  'Strict-Transport-Security': 'max-age=31536000',
  'X-Content-Type-Options': 'nosniff',
  'X-Frame-Options': 'DENY',
}

function sendText(response, status, message) {
  response.writeHead(status, {
    ...securityHeaders,
    'Cache-Control': 'no-store',
    'Content-Type': 'text/plain; charset=utf-8',
  })
  response.end(message)
}

createServer((request, response) => {
  if (request.method !== 'GET' && request.method !== 'HEAD') {
    response.setHeader('Allow', 'GET, HEAD')
    sendText(response, 405, 'Method Not Allowed')
    return
  }

  let pathname
  try {
    pathname = decodeURIComponent(new URL(request.url || '/', 'http://localhost').pathname)
  } catch {
    sendText(response, 400, 'Bad Request')
    return
  }

  const requestedPath = resolve(publicDirectory, `.${pathname}`)
  const isInsidePublicDirectory =
    requestedPath === publicDirectory || requestedPath.startsWith(`${publicDirectory}${sep}`)

  if (!isInsidePublicDirectory) {
    sendText(response, 403, 'Forbidden')
    return
  }

  let filePath = requestedPath
  try {
    const fileStats = statSync(filePath)
    if (fileStats.isDirectory()) filePath = resolve(filePath, 'index.html')
  } catch {
    if (extname(pathname)) {
      sendText(response, 404, 'Not Found')
      return
    }
    filePath = resolve(publicDirectory, 'index.html')
  }

  let fileStats
  try {
    fileStats = statSync(filePath)
    if (!fileStats.isFile()) throw new Error('Not a file')
  } catch {
    sendText(response, 404, 'Not Found')
    return
  }

  const extension = extname(filePath).toLowerCase()
  const isImmutableAsset = filePath.startsWith(resolve(publicDirectory, 'assets') + sep)
  response.writeHead(200, {
    ...securityHeaders,
    'Cache-Control': isImmutableAsset
      ? 'public, max-age=31536000, immutable'
      : extension === '.html'
        ? 'no-cache'
        : 'public, max-age=3600',
    'Content-Length': fileStats.size,
    'Content-Type': contentTypes[extension] || 'application/octet-stream',
  })

  if (request.method === 'HEAD') {
    response.end()
    return
  }

  const stream = createReadStream(filePath)
  stream.on('error', () => response.destroy())
  stream.pipe(response)
}).listen(port, '0.0.0.0', () => {
  console.log(`Static site listening on port ${port}`)
})
