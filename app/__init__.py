from fastapi import FastAPI
import structlog

logger = structlog.get_logger()

def create_app() -> FastAPI:
    app = FastAPI(
        title="Garv API",
        description="FastAPI application for Docker Demo",
        version="1.0.0",
        debug=True
    )
    return app 