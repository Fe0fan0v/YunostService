import datetime
from flask_login import UserMixin
import sqlalchemy
from sqlalchemy import orm
from .db_session import base


# class User(base, UserMixin):
#     __tablename__ = 'users'
#
#     id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
#     name = sqlalchemy.Column(sqlalchemy.String)
#     surname = sqlalchemy.Column(sqlalchemy.String)
#     patronymic = sqlalchemy.Column(sqlalchemy.String)
#     courses = sqlalchemy.Column(sqlalchemy.ARRAY(int), default=[])
#     birthday = sqlalchemy.Column(sqlalchemy.Date)
#     address = sqlalchemy.Column(sqlalchemy.String)
#     phone = sqlalchemy.Column(sqlalchemy.String)
#     email = sqlalchemy.Column(sqlalchemy.String)
#     health_class = sqlalchemy.Column(sqlalchemy.String)
#     school = sqlalchemy.Column(sqlalchemy.Integer)
#     s_class = sqlalchemy.Column(sqlalchemy.String)
#     role = sqlalchemy.Column(sqlalchemy.String, default='user')
#     registration_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now())
#     hashed_password = sqlalchemy.Column(sqlalchemy.String)


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


class Registration(base):
    __tablename__ = 'registration 22/23'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    #-------------информация о ребенке------------#
    child_name = sqlalchemy.Column(sqlalchemy.String)
    child_surname = sqlalchemy.Column(sqlalchemy.String)
    child_patronymic = sqlalchemy.Column(sqlalchemy.String)
    child_birthday = sqlalchemy.Column(sqlalchemy.Date)
    educational_institution = sqlalchemy.Column(sqlalchemy.String)
    edu_class = sqlalchemy.Column(sqlalchemy.String)
    health = sqlalchemy.Column(sqlalchemy.String)
    child_phone = sqlalchemy.Column(sqlalchemy.String)
    child_email = sqlalchemy.Column(sqlalchemy.String)
    child_residence = sqlalchemy.Column(sqlalchemy.String)
    # -------------информация о родителе------------#
    parent_name = sqlalchemy.Column(sqlalchemy.String)
    parent_surname = sqlalchemy.Column(sqlalchemy.String)
    parent_patronymic = sqlalchemy.Column(sqlalchemy.String)
    parent_birthday = sqlalchemy.Column(sqlalchemy.Date)
    parent_residence = sqlalchemy.Column(sqlalchemy.String)
    parent_work = sqlalchemy.Column(sqlalchemy.String)
    parent_phone = sqlalchemy.Column(sqlalchemy.String)
    parent_email = sqlalchemy.Column(sqlalchemy.String)
    full_family = sqlalchemy.Column(sqlalchemy.Boolean)
    large_family = sqlalchemy.Column(sqlalchemy.Boolean)
    without_parents = sqlalchemy.Column(sqlalchemy.Boolean)
    police_record = sqlalchemy.Column(sqlalchemy.Boolean)
    resident = sqlalchemy.Column(sqlalchemy.Boolean)
    second_parent_fio = sqlalchemy.Column(sqlalchemy.String)
    second_parent_phone = sqlalchemy.Column(sqlalchemy.String)
