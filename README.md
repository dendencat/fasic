# SwipeTune Monorepo (MVP scaffold)

This repository contains the planned monorepo for SwipeTune.

Structure (scaffolded):

```
apps/
  server/        # FastAPI server (T1: /health only)
    app/
    tests/
  mobile/        # Expo RN app (Hello + playback UI frame)
infra/           # docker-compose for Postgres + MinIO
```

## Getting Started

1) Copy env

```
cp .env.example .env
```

2) Start infra (Postgres + MinIO)

```
make up
```

3) Run API (developer machine)

```
cd apps/server
# Create venv and install deps (example)
python -m venv .venv && source .venv/bin/activate
pip install -e .
uvicorn app.main:app --reload --port 8080
```

4) Mobile app (developer machine)

```
cd apps/mobile
pnpm install
pnpm expo start

Expo client expects `EXPO_PUBLIC_API_BASE` to point to the server (see `.env.example`).
```

## OpenAPI

```
make gen-openapi
```

This writes `apps/server/OPENAPI.json` from the running FastAPI app definition.
