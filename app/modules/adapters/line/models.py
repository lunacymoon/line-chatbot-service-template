from typing import Optional

from app.constants.pydantic_model import BaseModel


class UserVerifyResponseModel(BaseModel):
    scope: str
    client_id: str
    expires_in: int


class RetrieveUserProfileModel(BaseModel):
    user_id: Optional[str]
    display_name: Optional[str]
    picture_url: Optional[str]
    status_message: Optional[str]
