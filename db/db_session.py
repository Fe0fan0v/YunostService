from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec
from sqlalchemy.orm import sessionmaker
from env import pg_login, pg_password

base = dec.declarative_base()

__factory = None


def global_init():
    global __factory

    if __factory:
        return

    conn_str = f'postgresql://{pg_login}:{pg_password}@localhost:5432/yunost'
    print(f"Подключение к базе данных по адресу {conn_str}")

    engine = create_engine(conn_str, echo=False)
    __factory = sessionmaker(bind=engine)

    from . import __all_models

    base.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()