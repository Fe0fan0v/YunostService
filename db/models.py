import sqlalchemy
from transliterate import translit
from string import ascii_letters, digits

from .db_session import base


class Course(base):
    __tablename__ = 'courses'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    focus = sqlalchemy.Column(sqlalchemy.String)
    direction = sqlalchemy.Column(sqlalchemy.String)
    area = sqlalchemy.Column(sqlalchemy.String)
    teachers = sqlalchemy.Column(sqlalchemy.ARRAY(sqlalchemy.String))  # список педагогов
    age_from = sqlalchemy.Column(sqlalchemy.Integer)
    age_to = sqlalchemy.Column(sqlalchemy.Integer)
    schedule = sqlalchemy.Column(sqlalchemy.JSON)  # расписание, пример: {"1": "ПН 15:25-17:10"}
    description = sqlalchemy.Column(sqlalchemy.Text)
    free = sqlalchemy.Column(sqlalchemy.Boolean)
    code = sqlalchemy.Column(sqlalchemy.Integer)
    counter = sqlalchemy.Column(sqlalchemy.Integer, default=0)

    def name_to_id(self):
        translit_name = translit(self.name, language_code='ru', reversed=True)
        translit_name = '_'.join(translit_name.split())
        return ''.join(filter(lambda c: c in ascii_letters + digits + '_', translit_name))


class Registration(base):
    __tablename__ = 'registration 22/23'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    # -------------информация о ребенке------------#
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
    courses = sqlalchemy.Column(sqlalchemy.JSON)  # {'название курса': 'номер группы'}
