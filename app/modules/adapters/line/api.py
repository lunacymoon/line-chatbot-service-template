from typing import Optional

from app.constants.exception import UnauthorizedBehaviorException
from app.modules.adapters.line.models import (
    RetrieveUserProfileModel,
    UserVerifyResponseModel,
)
from app.modules.adapters.line.util import get_request_async_client


class LineClient:
    def __init__(self, user_access_token: Optional[str] = None, channel_access_token: Optional[str] = None):
        self._channel_access_token = channel_access_token
        self._link_token = None
        self._user_access_token = user_access_token

    @property
    def _auth_headers(self) -> dict:
        if not self._channel_access_token:
            raise UnauthorizedBehaviorException('Channel Access Token cannot be None')
        return {'Content-Type': 'application/json', 'Authorization': f"Bearer {self._channel_access_token}"}

    @property
    def _user_auth_headers(self) -> dict:
        if not self._user_access_token:
            raise UnauthorizedBehaviorException('User Access Token cannot be None')
        return {'Authorization': f"Bearer {self._user_access_token}"}

    async def get_user_link_token(self, user_id: str):
        async with get_request_async_client(
            headers=self._auth_headers,
        ) as client:
            response = await client.post(f'/v2/bot/user/{user_id}/linkToken')

            response.raise_for_status()

            self._link_token = response.json()['linkToken']

    async def verify_access_token(self) -> UserVerifyResponseModel:
        async with get_request_async_client() as client:
            response = await client.get(f'/oauth2/v2.1/verify?access_token={self._user_access_token}')

            response.raise_for_status()
            verify_info = response.json()

            return UserVerifyResponseModel(
                scope=verify_info.get('scope'),
                client_id=verify_info.get('client_id'),
                expires_in=verify_info.get('expires_in'),
            )

    async def retrieve_user_profile(self) -> RetrieveUserProfileModel:
        async with get_request_async_client(headers=self._user_auth_headers) as client:
            response = await client.get('/v2/profile')

            response.raise_for_status()
            user_profile = response.json()

            return RetrieveUserProfileModel(
                user_id=user_profile.get('userId'),
                display_name=user_profile.get('displayName', None),
                picture_url=user_profile.get('picture_url', None),
                status_message=user_profile.get('statusMessage', None),
            )
