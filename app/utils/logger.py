import asyncio
import logging
import logging.config

import boto3
import watchtower
from fastapi import Request
from starlette.types import Message

from configs.log import LogConfig

APP_LOGGER = logging.getLogger('app')


def make_logger(region_name: str):
    logging.config.dictConfig(LogConfig().dict())

    handler = watchtower.CloudWatchLogHandler(
        boto3_client=boto3.client('logs', region_name=region_name), log_group_name='app'
    )
    APP_LOGGER.addHandler(handler)

    return APP_LOGGER


def set_body(request: Request, body: bytes):
    def receive() -> Message:
        return {'type': 'http.request', 'body': body}

    request._receive = receive


def log_info(request, response):
    logger = logging.getLogger('app.fastapi')
    logger.info(f'{request.method} {request.url}')
    if request.method == 'POST':
        request_body = asyncio.run(request.body())
        set_body(request, request_body)
        logger.info(f'Request Body: {request_body}')
    if response.body:
        logger.info('Response: ' + response.body.decode('utf8').replace('\"', '\'').replace(':', ': '))
