import datetime
import re
from numbers import Number

from openpyxl import load_workbook
from thefuzz import process
import pandas as pd
from sqlalchemy.orm.attributes import flag_dirty

from db.db_session import init_db, db_session
from db.models import Course
from env import path_to_xldata

pd.set_option('display.max_colwidth', 80)
FILENAME = path_to_xldata

keys = ['name', 'age_from', 'age_to', 'focus', 'direction', 'description',
        'teachers', 'area', 'free', 'code', 'schedule', 'counter']


def clear(s):
    if s is None:
        return
    return ' '.join(s.split())


def correct_area(area):
    correct = {'Макеева': 'пр. Макеева, 39',
               'Разина': 'ул. Ст. Разина, 4',
               'Первомайская': 'ул. Первомайская, 9',
               'Марта': 'ул. 8-е Марта, 147',
               'Октября': 'пр. Октября, 21'}
    for k in correct:
        if k in area:
            return correct[k]
    return ' '.join(area.split())


def get_age(data):
    if isinstance(data, Number):
        return int(data), int(data)
    if isinstance(data, datetime.datetime):
        return data.day, data.month
    attempt = re.search('(\d*)\+', data)
    if attempt:
        age_from = attempt.groups()[0]
        return int(age_from), 18
    attempt = re.search('(\d*)\s*-\s*(\d*)\s*[\w\W]*', data)
    if attempt:
        age_from, age_to = attempt.groups()
        return int(age_from), int(age_to)


def create_or_edit_course(name, age, focus, direction, description, teachers, area, free, code, *schedule):
    code = int(code) if code else -1
    if not all((name, age, focus, direction, description, teachers, area, free, code)):
        return None
    schedule = dict(filter(lambda pair: pair[1], zip((str(i) for i in range(1, 11)),
                                                     (clear(value) for value in schedule))))
    if not schedule:
        return None
    name = name.strip()
    age_from, age_to = get_age(age)
    teachers = teachers.split(',')
    focus = focus.upper()
    direction = direction.upper()
    area = correct_area(area)
    free = free is None or free.strip().lower() == 'бюджет'

    template = '^^'.join(map(str, (name, age_from, age_to, description, ','.join(teachers), area)))
    fuzzy_result = process.extractOne(template, keys_courses)  # нечеткий поиск
    if fuzzy_result[1] < 95:
        data = {'Было': fuzzy_result[0].split('^^'), 'Новый': (name, age_from, age_to, description, ','.join(teachers), area)}
        df = pd.DataFrame(data)
        print(df)
        while (choice := input('Что делать (1-принять изменения, 2-новый, 3-вручную):').strip()) not in ('1','2','3'):
            print('Некорректный ввод')
        if choice == '1':
            key = tuple(fuzzy_result[0].split('^^'))
            course_id = courses[key]
            course = db_session.query(Course).get(course_id)
            course.name = name
            course.age_from = age_from
            course.age_to = age_to
            course.focus = focus
            course.direction = direction
            course.description = description
            course.teachers = teachers
            course.area = area
            course.free = free
            course.code = code
            course.schedule = schedule
            flag_dirty(course)
            print(f'Изменен. id: {course_id}')
        elif choice == '2':
            course = Course(**dict(zip(keys, (name, age_from, age_to, focus, direction, description, teachers,
                                              area, free, code, schedule))))
            db_session.add(course)
            print('Новая запись')
        else:
            key = tuple(fuzzy_result[0].split('^^'))
            manual.append((name, courses[key]))
            print('Отложено на потом')
    else:
        key = tuple(fuzzy_result[0].split('^^'))
        course_id = courses[key]
        course = db_session.query(Course).get(course_id)
        course.name = name
        course.age_from = age_from
        course.age_to = age_to
        course.focus = focus
        course.direction = direction
        course.description = description
        course.teachers = teachers
        course.area = area
        course.free = free
        course.code = code
        course.schedule = schedule
        flag_dirty(course)
        print(f'Изменен курс {name}, id: {course_id}')
    db_session.commit()

init_db()
courses = {(c.name, str(c.age_from), str(c.age_to), c.description, ','.join(c.teachers), c.area): c.id
           for c in db_session.query(Course).all()}
keys_courses = ['^^'.join(c) for c in courses]
create_counter = 0
total_counter = 0
wb = load_workbook(FILENAME)
ws = wb.active
manual = []
for row in filter(lambda r: r[0].value, ws.iter_rows(min_row=5)):
    if len(list(filter(lambda c: c.value, row))) <= 1:
        continue
    total_counter += 1
    create_or_edit_course(*(cell.value for cell in row))
    print()
print('Разобрать вручную:')
for name, cid in manual:
    print(name, 'Вероятный id:', cid)
