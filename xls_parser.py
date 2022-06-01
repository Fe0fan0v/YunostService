import datetime
import re
from numbers import Number

from openpyxl import load_workbook
from thefuzz import process

from db.db_session import global_init, create_session
from db.models import Course
from env import path_to_xldata

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


def create_course(name, age, focus, direction, description, teachers, area, free, code, *schedule):
    if not code:
        code = -1
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
    code = int(code) if code else 0

    if not courses:  # таблица курсов была пуста - сразу создаем новый
        ratio = 0
    else:
        find_name, ratio = process.extractOne(name, [c[0] for c in courses])  # нечеткий поиск
    if ratio > 90:  # на 90% и более похожее название
        relevant_name = list(filter(lambda t: t[0] == find_name, courses))
        # есть курсы с одинаковыми названиями, отличаются либо возрастом, либо преподавателями
        if len(relevant_name) > 1:
            relevant_age = list(filter(lambda t: (t[1], t[2]) == (age_from, age_to), relevant_name))
            if len(relevant_age) == 1:
                key = relevant_age[0]
            else:
                relevant_all = list(filter(lambda t: t == (find_name, age_from, age_to, ','.join(teachers)), relevant_name))
                if relevant_all:
                    key = relevant_all[0]
                else:
                    course = Course(**dict(zip(keys, (name, age_from, age_to, focus, direction, description, teachers,
                                                      area, free, code, schedule, 0))))
                    db_session.add(course)
                    print(f'Ничего не найдено. Создан курс "{name}", counter = 0')
                    return True
        else:
            key = relevant_name[0]
        counter = courses[key]
    else:
        counter = 0
    course = Course(**dict(zip(keys, (name, age_from, age_to, focus, direction, description, teachers,
                                      area, free, code, schedule, counter))))
    db_session.add(course)
    print(f'Создан курс "{name}", counter = {counter}')
    return True


global_init()
db_session = create_session()
courses = {(c.name, c.age_from, c.age_to, ','.join(c.teachers)): c.counter for c in db_session.query(Course).all()}
print(len(courses))
db_session.query(Course).delete()
create_counter = 0
total_counter = 0
wb = load_workbook(FILENAME)
ws = wb.active
for row in filter(lambda r: r[0].value, ws.iter_rows(min_row=5)):
    if len(list(filter(lambda c: c.value, row))) <= 1:
        continue
    total_counter += 1
    result = create_course(*(cell.value for cell in row))
    if result:
        create_counter += 1
    print()
db_session.commit()
print(f'Создано: {create_counter}, всего прочитано строк: {total_counter}')
