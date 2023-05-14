import sqlalchemy
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from transliterate import translit
from string import ascii_letters, digits
from .db_session import base


class Course(base, SerializerMixin):
    __tablename__ = 'courses_23'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    focus = sqlalchemy.Column(sqlalchemy.String)
    direction = sqlalchemy.Column(sqlalchemy.String)
    area = sqlalchemy.Column(sqlalchemy.String)
    teachers = sqlalchemy.Column(sqlalchemy.ARRAY(sqlalchemy.String))  # список педагогов
    age_from = sqlalchemy.Column(sqlalchemy.Integer)
    age_to = sqlalchemy.Column(sqlalchemy.Integer)
    groups = relationship("Group", back_populates="group_course", lazy='subquery')
    certificate = sqlalchemy.Column(sqlalchemy.Boolean)
    description = sqlalchemy.Column(sqlalchemy.Text)
    free = sqlalchemy.Column(sqlalchemy.Boolean)
    code = sqlalchemy.Column(sqlalchemy.Integer)
    counter = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    records = relationship("Association", back_populates="course")

    def name_to_id(self):
        translit_name = translit(self.name, language_code='ru', reversed=True)
        translit_name = '_'.join(translit_name.split())
        return ''.join(filter(lambda c: c in ascii_letters + digits + '_', translit_name))

    def str_to_url(self):
        return self.name.replace('+', '%2B').replace('#', '23%')

    def __repr__(self):
        return f"""'name': {self.name}, 'area': {self.area}, 'focus': {self.focus}, 'direction': {self.direction},
                'description': {self.description}, 'teachers': {self.teachers}, 'age_from': {self.age_from},
                'age_to': {self.age_to}, 'free': {self.free}, 'code': {self.code}, 'schedule': {self.schedule}"""


# class Registration(base, SerializerMixin):
#     __tablename__ = 'registration 22/23'
#
#     id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
#     # -------------информация о ребенке------------#
#     child_name = sqlalchemy.Column(sqlalchemy.String)
#     child_surname = sqlalchemy.Column(sqlalchemy.String)
#     child_patronymic = sqlalchemy.Column(sqlalchemy.String)
#     child_birthday = sqlalchemy.Column(sqlalchemy.Date)
#     educational_institution = sqlalchemy.Column(sqlalchemy.String)
#     edu_class = sqlalchemy.Column(sqlalchemy.String)
#     health = sqlalchemy.Column(sqlalchemy.String)
#     child_phone = sqlalchemy.Column(sqlalchemy.String)
#     child_email = sqlalchemy.Column(sqlalchemy.String)
#     child_residence = sqlalchemy.Column(sqlalchemy.String)
#     # -------------информация о родителе------------#
#     parent_name = sqlalchemy.Column(sqlalchemy.String)
#     parent_surname = sqlalchemy.Column(sqlalchemy.String)
#     parent_patronymic = sqlalchemy.Column(sqlalchemy.String)
#     parent_birthday = sqlalchemy.Column(sqlalchemy.Date)
#     parent_residence = sqlalchemy.Column(sqlalchemy.String)
#     parent_work = sqlalchemy.Column(sqlalchemy.String)
#     parent_phone = sqlalchemy.Column(sqlalchemy.String)
#     parent_email = sqlalchemy.Column(sqlalchemy.String)
#     full_family = sqlalchemy.Column(sqlalchemy.Boolean)
#     large_family = sqlalchemy.Column(sqlalchemy.Boolean)
#     without_parents = sqlalchemy.Column(sqlalchemy.Boolean)
#     police_record = sqlalchemy.Column(sqlalchemy.Boolean)
#     resident = sqlalchemy.Column(sqlalchemy.Boolean)
#     second_parent_fio = sqlalchemy.Column(sqlalchemy.String)
#     second_parent_phone = sqlalchemy.Column(sqlalchemy.String)
#     courses = sqlalchemy.Column(sqlalchemy.JSON)  # {'название курса': 'номер группы'}
#
#     def as_dict(self):
#         dic = self.__dict__
#         dic.pop('_sa_instance_state')
#         return dic


class Record(base, SerializerMixin):
    __tablename__ = 'records_23'

    serialize_only = ('child_name', 'child_surname', 'child_patronymic', 'child_birthday',
                      'parent_name', 'parent_surname', 'parent_patronymic', 'parent_phone', 'parent_email',
                      'courses.course.name', 'courses.group')

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    # -------------информация о ребенке------------#
    child_name = sqlalchemy.Column(sqlalchemy.String)
    child_surname = sqlalchemy.Column(sqlalchemy.String)
    child_patronymic = sqlalchemy.Column(sqlalchemy.String)
    child_birthday = sqlalchemy.Column(sqlalchemy.Date)
    educational_institution = sqlalchemy.Column(sqlalchemy.String)
    edu_class = sqlalchemy.Column(sqlalchemy.String)
    health = sqlalchemy.Column(sqlalchemy.String)
    snils = sqlalchemy.Column(sqlalchemy.String)
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
    courses = relationship("Association", back_populates="record")


class Association(base, SerializerMixin):
    __tablename__ = "records_courses_23"
    record_id = sqlalchemy.Column('record_id', sqlalchemy.ForeignKey('records_23.id'), primary_key=True)
    course_id = sqlalchemy.Column('course_id', sqlalchemy.ForeignKey('courses_23.id'), primary_key=True)
    group = sqlalchemy.Column(sqlalchemy.String)
    comment = sqlalchemy.Column(sqlalchemy.String)
    course = relationship("Course", back_populates="records")
    record = relationship("Record", back_populates="courses")


class Group(base, SerializerMixin):
    __tablename__ = "groups_23"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    number = sqlalchemy.Column(sqlalchemy.Integer)
    course_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('courses_23.id'))
    schedule = sqlalchemy.Column(sqlalchemy.String)
    opened = sqlalchemy.Column(sqlalchemy.Boolean)
    group_course = relationship("Course", back_populates="groups")
