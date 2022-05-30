import datetime
import re
from numbers import Number

from openpyxl import load_workbook
from db.db_session import global_init, create_session
from db.models import Course

FILENAME = 'courses.xlsx'

keys = ['name', 'age', 'direction', 'description', 'teachers', 'area', 'free',
        *(str(i) for i in range(1, 11))]


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
    # pref, name, number = re.search('(пр\.|ул\.)\s*([^\s]*)[,\s]*(\d*)', area).groups()
    # return f'{pref} {name}, {number}'


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


global_init()
db_session = create_session()
wb = load_workbook(FILENAME)
ws = wb.active
for row in filter(lambda r: r[0].value, ws.iter_rows(min_row=5)):
    if len(list(filter(lambda c: c.value, row))) <= 1:
        continue
    data = dict(zip(keys, (cell.value for cell in row[:6])))
    if not all(data.values()):
        continue
    data['age_from'], data['age_to'] = get_age(data['age'])
    data.pop('age')
    data['teachers'] = data['teachers'].split(',')
    data['direction'] = data['direction'].upper()
    data['area'] = correct_area(data['area'])
    course = Course(**data)
    course.free = row[6].value is None or row[6].value.strip().lower() == 'бюджет'
    schedule = dict(filter(lambda pair: pair[1], zip(keys[7:], (clear(cell.value) for cell in row[7:]))))
    if not any(schedule.values()):
        continue
    course.schedule = schedule
    course.cube = row[0].fill.bgColor.rgb == 'FF00FFFF'
    db_session.add(course)
db_session.commit()
