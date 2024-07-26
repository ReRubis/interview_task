import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Callable

import uvicorn
from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.openapi.models import Response
from fastapi.responses import JSONResponse

from src.zypl_interview.config import config
from src.zypl_interview.exceptions import CustomBaseError
from src.zypl_interview.routes import router_factory

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """Lifspan event handler."""
    logger.debug("Preparing the app.")

    yield


def app_factory() -> FastAPI:
    """Builds the FastAPI app with the necessary middleware and routes."""
    app = FastAPI(lifespan=lifespan)

    app.include_router(router_factory())

    @app.middleware("http")
    async def handle_exceptions(
        request: Request, call_next: Callable
    ) -> Response | JSONResponse:
        try:
            response = await call_next(request)
            return response
        except CustomBaseError as e:
            json_data = jsonable_encoder({"message": e.message})
            return JSONResponse(json_data, status_code=e.status_code)
        except Exception as e:
            logging.error(e)
            json_data = jsonable_encoder({"message": "Server Error"})
            return JSONResponse(json_data, status_code=500)

    return app


app = app_factory()

if __name__ == "__main__":
    if config.DEBUG:
        uvicorn.run(app=app)
