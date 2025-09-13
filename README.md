# ferapp — Stage 0 (v0.1.0) starter

Monorepo на pnpm workspaces: API (Fastify, TypeScript) + Web (Next.js) + CI + Docker Compose с PostgreSQL.

## Быстрый старт
```bash
corepack enable
npm i -g pnpm@9
pnpm install --frozen-lockfile
# Запуск API
pnpm --filter @ferapp/api dev
# Запуск Web
pnpm --filter @ferapp/web dev
```

## Переменные окружения
Скопируйте `.env.example` в `.env` в соответствующих приложениях.

- `apps/api/.env.example` содержит `PORT` и `DATABASE_URL` (PostgreSQL)
- `apps/web/.env.example` содержит `API_URL`

## Тесты
```bash
pnpm -r test
```

## CI
GitHub Actions: build + lint + test. Релизы — по тегам `v*.*.*`.

## Docker Compose (PostgreSQL)
```bash
docker compose up -d
```

## Структура
```
ferapp/
  apps/
    api/   # Fastify API (TS), /health
    web/   # Next.js (TS), главная страница
  packages/
    shared/
  .github/workflows/ci.yml
  docker-compose.yml
```
