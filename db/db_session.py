import json

from sqlalchemy import create_engine
import sqlalchemy.ext.declarative as dec
from sqlalchemy.orm import sessionmaker, scoped_session
from env import pg_login, pg_password, db_name, db_host, db_port, conn_params

base = dec.declarative_base()
conn_str = f'postgresql://{pg_login}:{pg_password}@{db_host}:{db_port}/{db_name}' \
           f'{conn_params}'
print(f"Подключение к базе данных по адресу {conn_str}")
engine = create_engine(conn_str, convert_unicode=True, json_serializer=lambda obj: json.dumps(obj, ensure_ascii=False))


def create_db_session():
    db_session = scoped_session(sessionmaker(autocommit=False,
                                             autoflush=False,
                                             bind=engine,
                                             expire_on_commit=True))
    base.query = db_session.query_property()
    return db_session


def init_db():
    import db.models
    base.metadata.create_all(bind=engine)
