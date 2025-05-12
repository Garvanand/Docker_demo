from fastapi import FastAPI
from pythonjsonlogger import jsonlogger
import logging
from app.routes import router
from app.config import settings

logger = logging.getLogger()
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(name)s %(message)s')
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

def create_app() -> FastAPI:
    app = FastAPI(
        title="Garv API",
        description="FastAPI version of Garv's API",
        version="1.0.0",
        debug=settings.DEBUG
    )
    
    app.include_router(router)
    return app 