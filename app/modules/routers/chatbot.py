from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse

from app.constants.error_code import ErrorCode
from app.constants.exception import LineException
from app.constants.response import (
    default_responses,
    response_400,
)
from app.modules.adapters.line import (
    CHANNEL_ACCESS_TOKEN,
    AccountLinkEvent,
    InvalidSignatureError,
    LineClient,
    MessageEvent,
    ReplyMessageRequest,
    TextMessage,
    TextMessageContent,
    line_bot_api,
    line_webhook_handler,
)
from app.modules.routers import APIRoute
from configs.settings import settings

router = APIRouter(
    tags=['ChatBot'], responses=default_responses, route_class=APIRoute, prefix=f'/{settings.SERVICE_NAME}'
)


@router.post(
    '/callback',
    status_code=status.HTTP_200_OK,
    responses={**response_400(code=ErrorCode.LINE_SERVICE_ERROR, message='Missing Parameters')},
)
async def call_back(request: Request) -> JSONResponse:
    signature = request.headers['X-Line-Signature']
    body = await request.body()
    try:
        await line_webhook_handler.async_handle(body.decode(), signature)
    except InvalidSignatureError:
        raise LineException(http_status=status.HTTP_400_BAD_REQUEST, message='Missing Parameters')
    return JSONResponse(status_code=status.HTTP_200_OK, content='ok')


@line_webhook_handler.async_add(MessageEvent, message=TextMessageContent)
async def handle_message(event):
    messages = event.message.text
    user_id = event.source.user_id

    # TODO: handling incoming text message
    line_client = LineClient(channel_access_token=CHANNEL_ACCESS_TOKEN)
    await line_client.get_user_link_token(user_id=user_id)
    reply_text_message = 'hello'
    line_bot_api.reply_message_with_http_info(
        ReplyMessageRequest(reply_token=event.reply_token, messages=[TextMessage(text=reply_text_message)])
    )

@line_webhook_handler.async_add(AccountLinkEvent)
async def handling_account_link_event(event, signature):
    link_result = event.link.result
    link_nonce = event.link.nonce
    user_id = event.source.user_id

    if link_result == 'ok':
        # TODO: link our user with LINE account
        pass
        
