from app.constants.pydantic_model import ModelFactory
from app.modules.adapters.line.models import (
    RetrieveUserProfileModel,
    UserVerifyResponseModel,
)


class RetrieveUserProfileModelFactory(ModelFactory):
    __model__ = RetrieveUserProfileModel


class UserVerifyResponseModelFactory(ModelFactory):
    __model__ = UserVerifyResponseModel
