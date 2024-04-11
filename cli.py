# pylint: disable=import-outside-toplevel

from typing import Optional

import pytest
import typer
import uvicorn
from pytest import ExitCode
from sqlalchemy import MetaData, schema

from configs.settings import settings

app = typer.Typer()


@app.command()
def run(reload: Optional[bool] = False):
    uvicorn.run(
        'main:app',
        host=settings.HOST,
        port=settings.PORT,
        app_dir='app',
        reload=settings.RELOAD,
    )


@app.command()
def init_db():
    from app.utils.db import init_db

    init_db()


@app.command()
def reset_db():
    purge_db()
    create_schema()
    create_tables()


@app.command()
def purge_db():
    from app.utils.db import engine, get_schema_names
    from configs.database import DATABASE_DATABASE as DB_SCHEMA

    with engine.begin() as connection:
        existed_schemas = get_schema_names(conn=connection)
        if DB_SCHEMA in existed_schemas:
            metadata = MetaData()
            metadata.reflect(bind=engine, schema=DB_SCHEMA)
            print('Dropping db schema...')
            metadata.drop_all(bind=engine)
    engine.dispose()
    print('purge db successful.')


@app.command()
def create_schema():
    from app.utils.db import engine, get_schema_names
    from configs.database import DATABASE_DATABASE as DB_SCHEMA

    with engine.begin() as connection:
        existed_schemas = get_schema_names(conn=connection)
        # pylint: disable=no-member
        if engine.dialect.name == 'mysql' and DB_SCHEMA not in existed_schemas:
            print('Creating db schema...')
            connection.execute(schema.CreateSchema(DB_SCHEMA))
            print('create db schema successful.')

    engine.dispose()


@app.command()
def create_tables():
    from app.utils.db import SQLAlchemyBase as Base
    from app.utils.db import engine

    print('Creating db Tables...')
    for k in Base.metadata.tables.keys():  # pylint: disable=no-member
        print(f'  - {k}')

    # pylint: disable=no-member
    Base.metadata.create_all(engine)
    print('Create tables successful.')


@app.command()
def test(pytest_args: Optional[str] = typer.Option(None)):
    args = pytest_args.split(',') if pytest_args else []
    code = pytest.main(list(set(args)))

    if code != ExitCode.OK:
        raise typer.Exit(code)


if __name__ == '__main__':
    app()
