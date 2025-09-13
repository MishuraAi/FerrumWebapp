import { describe, it, expect } from 'vitest'
import Fastify from 'fastify'

describe('GET /health', () => {
  it('returns ok', async () => {
    const app = Fastify()
    app.get('/health', async () => ({ status: 'ok' }))
    const res = await app.inject({ method: 'GET', url: '/health' })
    expect(res.statusCode).toBe(200)
    expect(res.json()).toEqual({ status: 'ok' })
  })
})
