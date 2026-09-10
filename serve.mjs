import { createServer } from 'node:http'
import { createReadStream, statSync } from 'node:fs'
import { join, normalize, extname } from 'node:path'

const ROOT = process.argv[2]
const PORT = Number(process.argv[3])

const types = {
  '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.mjs': 'text/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8', '.json': 'application/json; charset=utf-8', '.svg': 'image/svg+xml',
  '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.gif': 'image/gif', '.webp': 'image/webp',
  '.ttf': 'font/ttf', '.ico': 'image/x-icon', '.txt': 'text/plain; charset=utf-8',
}

createServer((req, res) => {
  try {
    let pathname = decodeURIComponent(new URL(req.url || '/', 'http://localhost').pathname)
    if (pathname === '/' || pathname === '') pathname = '/index.html'
    const safe = join(ROOT, normalize(pathname).replace(/^(\.[\/\\])+/, ''))
    const st = statSync(safe)
    if (st.isDirectory()) { res.writeHead(301, { Location: pathname.replace(/\/?$/, '/') }); res.end(); return }
    res.writeHead(200, { 'content-type': types[extname(safe).toLowerCase()] || 'application/octet-stream' })
    createReadStream(safe).pipe(res)
  } catch {
    res.writeHead(404)
    res.end('not found')
  }
}).listen(PORT, '127.0.0.1', () => console.log('carpets-insiders on http://127.0.0.1:' + PORT))
