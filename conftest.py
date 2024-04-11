import pytest
from fastapi.testclient import TestClient
from sqlalchemy import event

from app.utils.db import Session, engine, get_db
from configs.settings import settings
from main import app


@pytest.fixture(scope='session')
def client(session):
    app.dependency_overrides[get_db] = lambda: session
    with TestClient(app, base_url=f'http://testserver/{settings.SERVICE_NAME}') as tc:
        yield tc


@pytest.fixture(scope='session')
def session():
    with engine.connect() as conn:
        conn.begin()
        conn.begin_nested()
        session = Session(bind=conn)

        @event.listens_for(session, 'after_transaction_end')
        def end_savepoint(session, transaction):
            if conn.closed:
                return
            if not conn.in_nested_transaction():
                conn.begin_nested()

        yield session

    engine.dispose()
