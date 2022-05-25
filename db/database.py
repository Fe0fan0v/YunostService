from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from env import pg_login, pg_password

conn_str = f'postgresql://{pg_login}:{pg_password}@localhost:5432/yunost'

engine = create_engine(conn_str, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
base = declarative_base()
base.query = db_session.query_property()


def init_db():
    import db.models
    base.metadata.create_all(bind=engine)
