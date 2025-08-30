from __future__ import annotations

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .db import init_engine
from .s3 import get_s3_client


APP_VERSION = os.getenv("APP_VERSION", "0.1.0")


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title="SwipeTune API", version=APP_VERSION)

    # CORS
    origins = [o.strip() for o in settings.allowed_origins.split(",") if o.strip()]
    if origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    @app.on_event("startup")
    def _on_startup() -> None:  # pragma: no cover - simple init
        # Initialize DB engine
        init_engine()
        # Prepare S3 client (optional at T1)
        get_s3_client()

    @app.get("/health")
    def health():
        return {"ok": True, "version": APP_VERSION}

    return app


app = create_app()

