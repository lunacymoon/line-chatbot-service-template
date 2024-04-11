from typing import Optional, Union

import httpx
from starlette import status

from app.constants.error_code import ErrorCode


class BaseException_(Exception):
    def __init__(
        self,
        code=ErrorCode.GENERAL_1001_UNEXPECTED_ERROR,
        http_status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message='unexpected error',
        data: Optional[dict] = None,
    ):
        self.code = code
        self.http_status = http_status
        self.message = message
        self.data = data or {}
        super().__init__(self.message)

    def __repr__(self):
        return f'Exception:CODE={self.code},MESSAGE={self.message},DATA={self.data}'


class LineException(BaseException_):
    http_status = status.HTTP_503_SERVICE_UNAVAILABLE
    code = ErrorCode.LINE_SERVICE_ERROR
    message = 'Line service is unavailable'

    def __init__(self, err: Union[str, httpx.HTTPStatusError, httpx.TimeoutException] = None, **kwargs):
        self.message = err if isinstance(err, str) else self.message
        self.data = (
            err.response.json() if isinstance(err, httpx.HTTPStatusError) and err.response.text else kwargs.get('data')
        )
        self.line_status_code = err.response.status_code if isinstance(err, httpx.HTTPStatusError) else None
        self.line_url = err.request.url if isinstance(err, (httpx.HTTPStatusError, httpx.TimeoutException)) else None
        super().__init__(code=self.code, http_status=self.http_status, message=self.message, data=self.data)


class LineTimeoutException(LineException):
    code = ErrorCode.LINE_TIMEOUT_ERROR
    message = 'Line service timeout'

    def __init__(self, **kwargs):
        super().__init__(code=self.code, message=self.message)


class ResourceNotFoundException(BaseException_):
    def __init__(self, subject: str):
        super().__init__(
            code=ErrorCode.GENERAL_1003_RESOURCE_NOT_FOUND,
            # NOTE: use 404 instead of 404 to fit FE error handling
            http_status=status.HTTP_400_BAD_REQUEST,
            message=f'{subject} not found',
        )


class UnauthorizedBehaviorException(BaseException_):
    def __init__(self, msg: str, code: ErrorCode = ErrorCode.GENERAL_1006_UNAUTHORIZED_BEHAVIOR):
        super().__init__(code=code, http_status=status.HTTP_403_FORBIDDEN, message=msg)
