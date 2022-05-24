import datetime
import random

import requests
from flask_security import hash_password

from models import Course, Person, Teacher, Parent, Student, User, Role, Group, Area, Direction
from security import user_datastore
from app import app
from db.db_session import create_session

directions_data = [('Изобразительное искусство', ''), ('Вокал', ''), ('Хореография', ''), ('Театр', ''), ('Цирк', ''),
                   ('Развивающая акробатика', ''), ('Журналистика', ''), ('Психология', ''),
                   ('Декоративно-прикладное творчество', 'валяние из шерсти, бисероплетение, текстильная кукла и др.'),
                   ('Конструирование, моделирование', ''), ('Спорт', ''), ('Шахматы', ''), ('Английский язык', ''),
                   ('Подготовка к школе', ''), ('Естественные науки', 'химия, биология, астрономия, геология'),
                   ('IT', 'программирование, робототехника, технический английский и др.'),
                   ('Фотография и видеография', '')]
areas_data = [('Пр-т Макеева, 39', 'Пр-т Октября, 21', 'Ул. Ст. Разина, 4', 'Ул. 8-е марта, 147',
               'ул. Первомайская, 9')]
courses = [(f'Новый курс {i}', f'Описание курса {i}') for i in range(1, 10)]


def get_users_data(n):
    api_url = 'https://api.randomdatatools.ru/'
    response = requests.get(api_url,
                            params={'count': n,
                                    'params': 'FirstName,LastName,FatherName,Login,Email,Phone,DateOfBirth,Address'})
    return response.json()


sess = create_session()
teachers = []
parents = []
with app.app_context():
    user = user_datastore.create_user(email='admin@ema.il', password=hash_password('admin'))
    user_datastore.add_role_to_user(user, user_datastore.find_or_create_role('admin'))

    for ud in get_users_data(10):
        user = user_datastore.create_user(email=ud['Email'],
                                          username=ud['Login'],
                                          password=hash_password('111'))
        user_datastore.add_role_to_user(user, user_datastore.find_or_create_role('teacher'))
        teacher = Teacher(name=ud['FirstName'],
                          surname=ud['LastName'],
                          patronymic=ud['FatherName'],
                          birthday=datetime.datetime.strptime(ud['DateOfBirth'], '%d.%m.%Y'),
                          phone=ud['Phone'],
                          residence=ud['Address'])
        teacher.user = user
        for i in range(1, 4):
            teacher.add_group(number=random.randint(1, 9),
                              schedule={"ПН": ["15:25", "17:10"], "СР": ["15:25", "17:10"]})
        teachers.append(teacher)

    for ud in get_users_data(10):
        user = user_datastore.create_user(email=ud['Email'],
                                          username=ud['Login'],
                                          password=hash_password('111'))
        user_datastore.add_role_to_user(user, user_datastore.find_or_create_role('parent'))
        parent = Parent(name=ud['FirstName'],
                        surname=ud['LastName'],
                        patronymic=ud['FatherName'],
                        birthday=datetime.datetime.strptime(ud['DateOfBirth'], '%d.%m.%Y'),
                        phone=ud['Phone'],
                        residence=ud['Address'],
                        work=ud['Address'][::-1],
                        full_family=bool(random.randint(0, 1)),
                        large_family=bool(random.randint(0, 1)),
                        without_parents=bool(random.randint(0, 1)),
                        police_record=bool(random.randint(0, 1)),
                        resident=bool(random.randint(0, 1)))
        parent.user = user
        for ud in get_users_data(2)[:random.randint(0, 2)]:
            child = parent.add_child(email=ud['Email'],
                             username=ud['Login'],
                             password=hash_password('111'),
                             name=ud['FirstName'],
                             surname=ud['LastName'],
                             patronymic=ud['FatherName'],
                             birthday=datetime.datetime.strptime(ud['DateOfBirth'], '%d.%m.%Y'),
                             phone=ud['Phone'],
                             residence=ud['Address'],
                             educational_institution=f'Школа №{random.randint(1, 50)}',
                             edu_class=f'{random.randint(1, 11)}',
                             health='здоров(а)')
            parent.assign(child, random.choice(random.choice(teachers).groups))
        parents.append(parent)

    user_datastore.commit()

directions = [Direction(name=n, description=d) for n, d in directions_data]
areas = [Area(name=a) for a in areas_data]

courses = [Course(name=n,
                  description=d,
                  direction=random.choice(directions),
                  area=random.choice(areas),
                  teachers=random.choices(teachers, k=random.randint(1, 3)),
                  age_from=random.randint(6, 12),
                  age_to=random.randint(12, 18)) for n, d in courses]

for d in directions:
    sess.add(d)
for a in areas:
    sess.add(a)
for t in teachers:
    sess.add(t)
for p in parents:
    sess.add(p)
for c in courses:
    sess.add(c)
sess.commit()
