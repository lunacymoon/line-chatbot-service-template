import uvicorn

from app import create_app
from configs.settings import settings

app = create_app()

if __name__ == '__main__':
    uvicorn.run('main:app', host=settings.HOST, port=settings.PORT, app_dir='app', reload=settings.RELOAD)
