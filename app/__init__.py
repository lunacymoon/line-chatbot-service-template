from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.constants.exception_handler import add_exception_handlers
from app.utils.logger import make_logger
from configs.settings import settings


def create_app():
    app = FastAPI()
    app.logger = make_logger(settings.REGION_NAME)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    add_exception_handlers(app)

    # List Routers Here!
    from app.modules.routers.chatbot import router as chatbot_router
    app.include_router(chatbot_router)

    return app
