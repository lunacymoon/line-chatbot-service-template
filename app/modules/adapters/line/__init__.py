import asyncio

from linebot.models import AccountLinkEvent
from linebot.v3 import WebhookHandler as WebhookHandler_
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    ApiClient,
    Configuration,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
)
from linebot.v3.webhook import LOGGER, PY3, inspect
from linebot.v3.webhooks import MessageEvent, TextMessageContent

from configs.settings import settings

from .api import LineClient

CHANNEL_SECRET = settings.CHANNEL_SECRET
CHANNEL_ACCESS_TOKEN = settings.CHANNEL_ACCESS_TOKEN


class AsyncWebhookHandler(WebhookHandler_):
    def __init__(self, channel_secret):
        super().__init__(channel_secret)

    async def process_payload(self, payload):
        for event in payload.events:
            func = None
            key = None

            if isinstance(event, MessageEvent):
                key = self.__get_handler_key(event.__class__, event.message.__class__)
                func = self._handlers.get(key, None)

            if func is None:
                key = self.__get_handler_key(event.__class__)
                func = self._handlers.get(key, None)

            if func is None:
                func = self._default

            if func is None:
                LOGGER.info('No handler of ' + key + ' and no default handler')
            else:
                await self.__invoke_async_func(func, event, payload)

    async def async_handle(self, body, signature):
        payload = self.parser.parse(body, signature, as_payload=True)
        await self.process_payload(payload)

    @classmethod
    async def __invoke_async_func(cls, func, event, payload):
        (has_varargs, args_count) = cls.__get_args_count(func)
        if asyncio.iscoroutinefunction(func):
            if has_varargs or args_count == 2:
                await func(event, payload.destination)
            elif args_count == 1:
                await func(event)
            else:
                await func()
        else:
            func(event, payload)

    def async_add(self, event, message=None):
        def decorator(func):
            if isinstance(message, (list, tuple)):
                for it in message:
                    self.__add_async_handler(func, event, message=it)
            else:
                self.__add_async_handler(func, event, message=message)
            return func

        return decorator

    def async_default(self):
        def decorator(func):
            self._default = func
            return func

        return decorator

    def __add_async_handler(self, func, event, message=None):
        if not asyncio.iscoroutinefunction(func):
            raise ValueError(f"Function {func.__name__} is not asynchronous.")
        if event:
            key = self.__get_handler_key(event, message)
            self._handlers[key] = func
        else:
            self._default = func

    @staticmethod
    def __get_args_count(func):
        if PY3:
            arg_spec = inspect.getfullargspec(func)
            return (arg_spec.varargs is not None, len(arg_spec.args))
        else:
            arg_spec = inspect.getargspec(func)
            return (arg_spec.varargs is not None, len(arg_spec.args))

    @staticmethod
    def __get_handler_key(event, message=None):
        if message is None:
            return event.__name__
        else:
            return event.__name__ + '_' + message.__name__


line_bot_api = MessagingApi(api_client=ApiClient(configuration=Configuration(access_token=CHANNEL_ACCESS_TOKEN)))
line_webhook_handler = AsyncWebhookHandler(CHANNEL_SECRET)
