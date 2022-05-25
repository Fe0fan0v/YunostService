from flask_security import UserMixin, RoleMixin, hash_password
from sqlalchemy import Table, Column, String, Text, Integer, Date, DateTime, Boolean, \
    JSON, ForeignKey
from sqlalchemy.orm import relationship, backref

from .database import base, db_session


class RolesUsers(base):
    __tablename__ = 'roles_users'
    id = Column(Integer(), primary_key=True)
    user_id = Column('user_id', Integer(), ForeignKey('user.id'))
    role_id = Column('role_id', Integer(), ForeignKey('role.id'))


class Role(base, RoleMixin):
    __tablename__ = 'role'
    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))


class User(base, UserMixin):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    username = Column(String(255), unique=True, nullable=True)
    password = Column(String(255), nullable=False)

    last_login_at = Column(DateTime())
    current_login_at = Column(DateTime())
    last_login_ip = Column(String(100))
    current_login_ip = Column(String(100))
    login_count = Column(Integer)
    active = Column(Boolean())
    fs_uniquifier = Column(String(255), unique=True, nullable=False)
    confirmed_at = Column(DateTime())
    roles = relationship('Role', secondary='roles_users',
                         backref=backref('users', lazy='dynamic'))

    def make_person(self, **kwargs):
        person = Person(**keys_only_for(Person, **kwargs))
        person.user = self
        db_session.add(person)
        return person

    def make_teacher(self, **kwargs):
        self.make_person(**kwargs)
        teacher = Teacher(**keys_only_for(Teacher, **kwargs))
        teacher.user = self
        db_session.add(teacher)
        return teacher

    def make_student(self, **kwargs):
        self.make_person(**kwargs)
        student = Student(**keys_only_for(Student, **kwargs))
        student.user = self
        db_session.add(student)
        return student

    def make_parent(self, **kwargs):
        self.make_person(**kwargs)
        parent = Parent(**keys_only_for(Parent, **kwargs))
        parent.user = self
        db_session.add(parent)
        return parent


class Course(base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    direction_id = Column(Integer, ForeignKey('directions.id'))
    direction = relationship('Direction', back_populates='courses')
    area_id = Column(Integer, ForeignKey('areas.id'))
    area = relationship('Area', back_populates='courses')
    teachers = relationship('Teacher', secondary='teachers_courses', backref="courses")
    age_from = Column(Integer)
    age_to = Column(Integer)
    description = Column(Text)


class Group(base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True, autoincrement=True)
    number = Column(Integer)
    teacher_id = Column(Integer, ForeignKey('teachers.id'))
    teacher = relationship('Teacher', back_populates='groups')
    schedule = Column(JSON)  # {"ПН": ["15:25", "17:10"], "СР": ["15:25", "17:10"]}
    students = relationship('Student', secondary='students_groups', backref='groups')


class Person(base):
    __tablename__ = 'persons'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', backref=backref('person', uselist=False))

    name = Column(String(255))
    surname = Column(String(255))
    patronymic = Column(String(255))
    birthday = Column(Date)
    phone = Column(String)
    residence = Column(String)


class Student(base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', backref=backref('student', uselist=False))

    educational_institution = Column(String)
    edu_class = Column(String)
    health = Column(String)
    parent_id = Column(Integer, ForeignKey('parents.id'))
    parent = relationship('Parent', back_populates='children')
    temp_password = Column(String)


class Teacher(base):
    __tablename__ = 'teachers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', backref=backref('teacher', uselist=False))

    groups = relationship('Group', back_populates='teacher')

    def add_group(self, **kwargs):
        group = Group(**kwargs)
        group.teacher = self
        db_session.add(group)


class Parent(base):
    __tablename__ = 'parents'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', backref=backref('parent', uselist=False))

    work = Column(String)
    full_family = Column(Boolean)
    large_family = Column(Boolean)
    without_parents = Column(Boolean)
    police_record = Column(Boolean)
    resident = Column(Boolean)
    second_parent_fio = Column(String)
    second_parent_phone = Column(String)
    children = relationship('Student', back_populates='parent')

    @staticmethod
    def add_child(**kwargs):
        from security import user_datastore
        temp_password = '444'  # todo: generate
        user = user_datastore.create_user(email=kwargs['email'],
                                          username=kwargs['username'],
                                          password=hash_password(temp_password))
        user_datastore.add_role_to_user(user, user_datastore.find_or_create_role('student'))
        db_session.add(user)
        stud = user.make_student(**keys_only_for(Student, **kwargs))
        return stud

    def get_child(self, index):
        return self.children[index]

    @staticmethod
    def assign(child, group):
        group.students.append(child)


class Area(base):
    __tablename__ = 'areas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    courses = relationship('Course', back_populates='area')


class Direction(base):
    __tablename__ = 'directions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    description = Column(String)
    courses = relationship('Course', back_populates='direction')


teachers_courses = Table('teachers_courses', base.metadata,
                         Column('teacher_id', ForeignKey('teachers.id'), primary_key=True),
                         Column('course_id', ForeignKey('courses.id'), primary_key=True))

students_groups = Table('students_groups', base.metadata,
                        Column('student_id', ForeignKey('students.id'), primary_key=True),
                        Column('group_id', ForeignKey('groups.id'), primary_key=True))


def keys_only_for(cls, **kwargs):
    res = {k: v for k, v in kwargs.items()
           if k in filter(lambda x: not x.startswith('_') and x != 'metadata', dir(cls))}
    print(cls.__name__, res)
    return res
