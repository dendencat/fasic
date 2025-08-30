PROJECT_ROOT := $(shell pwd)

.PHONY: up down gen-openapi test

up:
	@docker compose -f infra/docker-compose.yml --env-file .env up -d

down:
	@docker compose -f infra/docker-compose.yml --env-file .env down -v

# Export OpenAPI spec from FastAPI app
gen-openapi:
	@cd apps/server && \
	python - <<'PY'
from app.main import app
import json
open('OPENAPI.json','w').write(json.dumps(app.openapi(), indent=2))
print('Wrote apps/server/OPENAPI.json')
PY

# Run tests
test:
	@cd apps/server && python -m pytest

