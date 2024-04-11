from typing import Union

from pydantic import BaseModel
from starlette import status

from app.constants.error_code import ErrorCode


class ErrorMessage(BaseModel):
    code: Union[int, list[int]]
    message: str


default_responses: dict = {
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        'model': ErrorMessage,
        'description': 'Internal error',
        'content': {
            'application/json': {
                'example': {'code': ErrorCode.GENERAL_1001_UNEXPECTED_ERROR, 'message': 'internal error'}
            }
        },
    },
}


def response_400(code: Union[ErrorCode, list[ErrorCode]], message: str) -> dict:
    return {
        status.HTTP_400_BAD_REQUEST: {
            'model': ErrorMessage,
            'description': message,
            'content': {'application/json': {'example': {'code': code, 'message': message}}},
        }
    }


def response_503(subject: str) -> dict:
    return {
        status.HTTP_503_SERVICE_UNAVAILABLE: {
            'model': ErrorMessage,
            'description': f'{subject} service is unavailable',
            'content': {
                'application/json': {
                    'example': {
                        'code': ErrorCode.LINE_TIMEOUT_ERROR,
                        'message': 'Line service error or Line Service timeout error',
                    }
                }
            },
        }
    }


def response_400_entity_not_found(subject: str) -> dict:
    return {
        status.HTTP_400_BAD_REQUEST: {
            'model': ErrorMessage,
            'description': f'{subject} not found',
            'content': {
                'application/json': {
                    'example': {'code': ErrorCode.GENERAL_1003_RESOURCE_NOT_FOUND, 'message': 'resource not found'}
                }
            },
        }
    }
