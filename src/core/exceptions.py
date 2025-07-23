from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from loguru import logger
from sqlalchemy.exc import NoResultFound


class ExistingEmailError(Exception):
    pass


def setup_exception_handlers(app: FastAPI):
    @app.exception_handler(Exception)
    async def unicorn_exception_handler(request: Request, exc: Exception):
        logger.info("EXC handler")
        if isinstance(exc, NoResultFound):
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"error": exc.args[0]},
            )
        elif isinstance(exc, ExistingEmailError):
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"error": exc.args[0]},
            )
        elif isinstance(exc, Exception):
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": "Internal Server Error"},
            )
