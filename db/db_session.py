from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec
from sqlalchemy.orm import sessionmaker
from env import pg_login, pg_password, db_name, db_host, db_port, conn_params

base = dec.declarative_base()

__factory = None


def global_init():
    global __factory

    if __factory:
        return

    conn_str = f'postgresql://{pg_login}:{pg_password}@{db_host}:{db_port}/{db_name}' \
               f'{conn_params}'
    print(f"Подключение к базе данных по адресу {conn_str}")

    engine = create_engine(conn_str, echo=False, pool_size=20, max_overflow=10)
    __factory = sessionmaker(bind=engine)

    from . import __all_models

    base.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()
