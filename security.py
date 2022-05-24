from sqlalchemy.orm import scoped_session
from flask_security import Security, hash_password, SQLAlchemySessionUserDatastore

from db import db_session
from db.models import User, Role

sess = scoped_session(db_session.create_session)
user_datastore = SQLAlchemySessionUserDatastore(sess, User, Role)
security = Security(datastore=user_datastore)
