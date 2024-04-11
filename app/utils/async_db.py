import os
from asyncio import current_task
from typing import AsyncIterable

from sqlalchemy import MetaData, inspect
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio import AsyncSession as _AsyncSession
from sqlalchemy.ext.asyncio import async_scoped_session, create_async_engine
from sqlalchemy.future.engine import Connection
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy.orm.session import Session

from configs.database import (
    DATABASE_DATABASE,
    DATABASE_HOST,
    DATABASE_PASSWORD,
    DATABASE_PORT,
    DATABASE_USERNAME,
)

DEBUG = os.getenv('DEBUG', '')
IS_DEBUG: bool = True if DEBUG else False


db_url = URL.create(
    'mysql+aiomysql',
    username=DATABASE_USERNAME,
    password=DATABASE_PASSWORD,
    host=DATABASE_HOST,
    port=DATABASE_PORT,
    database=DATABASE_DATABASE,
    query={"charset": "utf8mb4"},
)

async_engine = create_async_engine(
    db_url,
    isolation_level='REPEATABLE READ',
    echo=IS_DEBUG,
    pool_recycle=3,
    pool_size=30,
    max_overflow=10,
    pool_pre_ping=True,
    connect_args={'connect_timeout': 5},
)


class AsyncSession(_AsyncSession):  # pylint: disable=abstract-method
    def __init__(self, *args, **kargs):
        super().__init__(sync_session_class=Session, *args, **kargs)

    async def set_flag_modified(self, instance, key: str):
        # https://docs.sqlalchemy.org/en/14/core/defaults.html
        # https://docs.sqlalchemy.org/en/14/orm/session_api.html#sqlalchemy.orm.attributes.flag_modified
        flag_modified(instance, key)


AsyncScopedSession = async_scoped_session(
    sessionmaker(
        async_engine,
        expire_on_commit=False,
        autoflush=False,
        class_=AsyncSession,
    ),
    scopefunc=current_task,
)


async def get_session() -> AsyncIterable[AsyncSession]:
    async with AsyncScopedSession() as session:
        yield session


def get_schema_names(conn: Connection) -> list[str]:
    inspector = inspect(conn)
    return inspector.get_schema_names()


SQLAlchemyBase = declarative_base(metadata=MetaData(schema=DATABASE_DATABASE))
