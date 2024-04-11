from contextlib import asynccontextmanager
from datetime import datetime

import httpx
from httpx import AsyncClient

from app.constants.exception import LineException, LineTimeoutException
from app.modules.adapters import API_TIMEOUT, LINE_API_URL
from app.utils.logger import APP_LOGGER


@asynccontextmanager
async def get_request_async_client(auth: httpx.Auth = None, headers: dict = None, timeout: float = None):
    async def log_request(request):
        APP_LOGGER.info(f"Line API Request: [{request.method}] {request.url} {datetime.now().strftime('%H:%M:%S.%f')}")

    async def log_response(response):
        APP_LOGGER.info(
            f"Line API Response: {response.status_code} [{response.request.method}]"
            f" {response.url} {datetime.now().strftime('%H:%M:%S.%f')}"
        )

    async with AsyncClient(
        auth=auth,
        headers=headers if headers else {'Content-Type': 'application/json'},
        base_url=LINE_API_URL,
        event_hooks={'request': [log_request], 'response': [log_response]},
        timeout=timeout if timeout else API_TIMEOUT,
    ) as client:
        try:
            yield client
        except httpx.HTTPStatusError as e:
            raise LineException(e)
        except httpx.TimeoutException as e:
            raise LineTimeoutException(str(e))
