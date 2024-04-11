import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from configs.database import DATABASE_URL
from configs.settings import settings


@pytest.fixture(scope='session')
def engine():
    return create_engine(DATABASE_URL)


@pytest.fixture()
def session(engine):
    connection = engine.connect()
    # begin the nested transaction
    transaction = connection.begin()
    # use the connection with the already started transaction
    session = Session(bind=connection)

    yield session

    session.close()
    # roll back the broader transaction
    transaction.rollback()
    # put back the connection to the connection pool
    connection.close()


@pytest.fixture()
def client(session):
    from app.utils.db import get_db
    from main import app

    app.dependency_overrides[get_db] = lambda: session
    return TestClient(app, base_url=f'http://testserver/{settings.SERVICE_NAME}')
