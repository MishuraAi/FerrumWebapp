import Fastify from 'fastify'
import { readFileSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
import { dirname, resolve } from 'node:path'

const __filename = fileURLToPath(import.meta.url)
const __dirname = dirname(__filename)
const pkg = JSON.parse(readFileSync(resolve(__dirname, '../package.json'), 'utf8'))

const server = Fastify({ logger: true })

server.get('/health', async () => {
  return { status: 'ok', service: 'ferapp-api', version: pkg.version }
})

const port = Number(process.env.PORT || 3001)
server.listen({ port, host: '0.0.0.0' }).catch((err) => {
  server.log.error(err)
  process.exit(1)
})
