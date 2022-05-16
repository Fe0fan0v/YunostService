import datetime
from flask_login import UserMixin
import sqlalchemy
from sqlalchemy import orm
from .db_session import base


class User(base, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    surname = sqlalchemy.Column(sqlalchemy.String)
    patronymic = sqlalchemy.Column(sqlalchemy.String)
    courses = sqlalchemy.Column(sqlalchemy.ARRAY(int), default=[])
    birthday = sqlalchemy.Column(sqlalchemy.Date)
    address = sqlalchemy.Column(sqlalchemy.String)
    phone = sqlalchemy.Column(sqlalchemy.String)
    email = sqlalchemy.Column(sqlalchemy.String)
    health_class = sqlalchemy.Column(sqlalchemy.String)
    school = sqlalchemy.Column(sqlalchemy.Integer)
    s_class = sqlalchemy.Column(sqlalchemy.String)
    role = sqlalchemy.Column(sqlalchemy.String, default='user')
    registration_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now())
    hashed_password = sqlalchemy.Column(sqlalchemy.String)


class Course(base):
    __tablename__ = 'courses'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    direction = sqlalchemy.Column(sqlalchemy.String)
    area = sqlalchemy.Column(sqlalchemy.String)
    teacher = sqlalchemy.Column(sqlalchemy.String)
    age_from = sqlalchemy.Column(sqlalchemy.Integer)
    age_to = sqlalchemy.Column(sqlalchemy.Integer)
    schedule = sqlalchemy.Column(sqlalchemy.JSON)
    description = sqlalchemy.Column(sqlalchemy.Text)
