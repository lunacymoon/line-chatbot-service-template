from typing import Callable

from fastapi import Request, Response, status
from fastapi.routing import APIRoute as APIRoute_
from starlette.background import BackgroundTask

from app.utils.logger import log_info


class APIRoute(APIRoute_):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            response = await original_route_handler(request)
            response.background = BackgroundTask(log_info, request, response)

            return response

        return custom_route_handler
