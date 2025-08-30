# Repository Guidelines

## Project Structure & Module Organization
- Monorepo layout (planned):
  - `apps/mobile` (Expo React Native)
  - `apps/server` (FastAPI + Postgres)
  - `packages/ui`, `packages/types` (shared modules)
  - `infra/` (docker-compose, ops), `.env.example`, `README.md`, `AGENT.md`
- Keep feature code close to its domain. Shared UI and types live under `packages/`. Server modules use `app/` with `routers/`, `models/`, `services/`, `deps/`.

## Build, Test, and Development Commands
- Infra: `make up` / `make down` — start/stop DB and S3 via Docker.
- Server:
  - `cd apps/server && uvicorn app.main:app --reload --port 8080` — run API.
  - `pytest -q` — run backend tests. `make gen-openapi` to export OpenAPI.
- Mobile:
  - `cd apps/mobile && pnpm install && pnpm expo start` — run Expo app.
  - Use the QR or simulator to load the client; set `EXPO_PUBLIC_API_BASE`.

## Coding Style & Naming Conventions
- Python: 4‑space indent; format with Black; imports via isort/Ruff; files `snake_case.py`; classes `PascalCase`; functions `snake_case`.
- TypeScript/React Native: 2‑space indent; Prettier + ESLint; components `PascalCase.tsx`; hooks `useThing.ts`; modules `kebab-case` dirs.
- Keep functions small; prefer pure utilities in `packages/`.

## Testing Guidelines
- Backend: `pytest`, tests under `apps/server/tests/` named `test_*.py`. Aim ≥80% line coverage for `app/`.
- Mobile: Jest + React Native Testing Library; tests beside source as `*.test.ts(x)`.
- Run locally before PR: server `pytest -q`; mobile `pnpm test`.

## Commit & Pull Request Guidelines
- Use Conventional Commits: `feat:`, `fix:`, `chore:`, `docs:`, `refactor:`.
- One logical change per PR; keep diffs focused and passing CI.
- PRs include: clear description, linked issues, API or UI screenshots/recordings, and notes on tests/docs updates.

## Security & Configuration Tips
- Never commit secrets. Copy `.env.example` → `.env` and fill locally.
- Client never holds server API keys; use signed URLs and server‑side proxies as defined in `AGENT.md`.
- Rotate credentials and restrict CORS to known dev origins.

Note: This repo currently contains planning (`AGENT.md`). As code is added, mirror the paths above and keep this guide updated.

