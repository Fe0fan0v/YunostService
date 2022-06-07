from sqlalchemy import create_engine
import sqlalchemy.ext.declarative as dec
from sqlalchemy.orm import sessionmaker, scoped_session
from env import pg_login, pg_password, db_name, db_host, db_port, conn_params


base = dec.declarative_base()
conn_str = f'postgresql://{pg_login}:{pg_password}@{db_host}:{db_port}/{db_name}' \
                f'{conn_params}'
print(f"Подключение к базе данных по адресу {conn_str}")
engine = create_engine(conn_str, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
base.query = db_session.query_property()


def init_db():
    import db.models
    base.metadata.create_all(bind=engine)
