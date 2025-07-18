from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from loguru import logger
from sqlalchemy.exc import NoResultFound


def setup_exception_handlers(app: FastAPI):
    @app.exception_handler(NoResultFound)
    async def unicorn_exception_handler(request: Request, exc: NoResultFound):
        logger.info("EXC handler")
        if isinstance(exc, NoResultFound):
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"error": exc.args[0]},
            )
