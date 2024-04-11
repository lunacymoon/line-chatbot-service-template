from fastapi import FastAPI, Request
from httpx import HTTPStatusError
from starlette import status
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import JSONResponse

from app.constants.error_code import ErrorCode
from app.constants.exception import BaseException_, LineException
from app.utils.logger import APP_LOGGER


def add_exception_handlers(app: FastAPI):
    @app.exception_handler(Exception)
    async def exception_handler(_: Request, exception: Exception):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={'message': 'internal error', 'code': ErrorCode.GENERAL_1001_UNEXPECTED_ERROR},
        )

    @app.exception_handler(HTTPStatusError)
    async def httpx_exception_handler(_: Request, exception: HTTPStatusError):
        try:
            return JSONResponse(
                status_code=exception.response.status_code,
                content={
                    'message': exception.response.json()['message'],
                    'code': ErrorCode.GENERAL_1001_UNEXPECTED_ERROR,
                },
            )
        except:  # noqa: E722
            return JSONResponse(
                status_code=exception.response.status_code,
                content={'message': exception.response.text, 'code': ErrorCode.GENERAL_1001_UNEXPECTED_ERROR},
            )

    @app.exception_handler(BaseException_)
    async def base_exception_handler(_: Request, exception: BaseException_):
        return JSONResponse(
            status_code=exception.http_status,
            content={
                'code': exception.code,
                'message': exception.message,
            },
        )

    @app.exception_handler(LineException)
    async def line_exception_handler(_: Request, exception: LineException):
        APP_LOGGER.error(
            {
                'message': exception.message,
                'data': exception.data,
                'line_status_code': exception.line_status_code,
                'line_url': exception.line_url,
            }
        )

        return JSONResponse(
            status_code=exception.http_status,
            content={'message': exception.message, 'code': exception.code},
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(_: Request, exception: StarletteHTTPException):
        return JSONResponse(
            status_code=exception.status_code,
            content={'message': exception.detail, 'code': ErrorCode.GENERAL_1007_NETWORK_ERROR},
        )
