from sqlalchemy.orm import scoped_session
from flask_security import Security, hash_password, SQLAlchemySessionUserDatastore

from db.database import db_session
from db.models import User, Role

user_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)
security = Security(datastore=user_datastore)
