import numpy
import sqlalchemy
from sqlalchemy import and_, update

from db.db_session import create_db_session
from db.models import Course, Group, Record
from flask import request
import pandas
import requests
from urllib.parse import urlencode


def show_courses(db_sess, access=False):
    courses_to_find = db_sess.query(Course).all()
    courses = []
    if access:
        for c in courses_to_find:
            if len([g for g in c.groups]) > 0:
                courses.append(c)
    else:
        for c in courses_to_find:
            if len([g for g in c.groups]) > 0 and all([group.opened for group in c.groups]):
                courses.append(c)
    areas = list(filter(lambda x: x is not None, list(set([course.area for course in courses]))))
    directions = list(filter(lambda x: x is not None, list(set([course.direction for course in courses]))))
    db_sess.close()
    return courses, areas, directions


def get_filter_criteria(db_sess, area: str, direction: str, cube: bool, success: bool):
    queries = {}
    if area != 'ВСЕ':
        queries['area'] = area
    if direction != 'ВСЕ':
        queries['direction'] = direction
    if cube:
        queries['code'] = 1
    if success:
        queries['code'] = 2
    result = ', '.join(f'Course.{key} == queries["{key}"]' for key in queries)
    if queries:
        records = eval('db_sess.query(Record).join("courses", "course").filter(and_(' + result + ')).all()')
    else:
        records = db_sess.query(Record).join("courses", "course").all()
    return records


def get_courses_from_table(table_url):
    base_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'
    public_key = table_url

    final_url = base_url + urlencode(dict(public_key=public_key))
    response = requests.get(final_url)
    download_url = response.json()['href']

    download_response = requests.get(download_url)
    with open('table.xlsx', 'wb') as f:
        f.write(download_response.content)

    data = pandas.read_excel('table.xlsx')
    return data


def update_database():
    data = get_courses_from_table('https://disk.yandex.ru/i/GlgIbYtajYasHQ').dropna(axis=0, thresh=5)
    db_session = create_db_session()
    courses = db_session.query(Course).all()
    for i, course in enumerate(data.itertuples()):
        if type(course.Программа) != float:
            existing_course = list(filter(lambda x: x.table_id == course.id, courses))
            if existing_course:
                existing_course = existing_course[0]
                print(f'Обновляю курс {existing_course.table_id}')
                existing_course.name = course.Программа.upper(),
                existing_course.focus = course.Направленность.upper(),
                existing_course.teachers = course.Педагоги.split(", ")
                if type(course.Возраст) != float:
                    if '-' in course.Возраст:
                        existing_course.age_from = course.Возраст.split("-")[0],
                        existing_course.age_to = course.Возраст.split("-")[1]
                    elif '+' in course.Возраст:
                        existing_course.age_from = course.Возраст[:-1]
                    else:
                        existing_course.age_from = course.Возраст
                if type(course.Направление) != float:
                    existing_course.direction = course.Направление.upper()
                if type(course.Форма) != float:
                    if course.Форма == 'Бюджет':
                        existing_course.free = True
                    elif course.Форма == 'Платно':
                        existing_course.free = False
                    if course.Форма == 'Сертификат':
                        existing_course.certificate = True
                    else:
                        existing_course.certificate = False
                if type(course.Описание) != float:
                    existing_course.description = course.Описание
                if course.Код == 2.0 or course.Код == 1.0:
                    existing_course.code = int(course.Код)
                if type(course.Площадка) != float:
                    existing_course.area = course.Площадка.upper()
                groups = db_session.query(Group).filter(Group.course_id == existing_course.id).all()
                for n in range(1, 7):
                    if type(eval(f'course.Расписание{n}')) != float:
                        existing_group = list(filter(lambda x: x.number == n, existing_course.groups))
                        if existing_group:
                            existing_group = existing_group[0]
                            existing_group.schedule = eval(f'course.Расписание{n}')
                            existing_group.opened = True if eval(f'course.Статус{n}') == 'Набор открыт' else False
                        else:
                            group = Group()
                            group.number = n
                            group.schedule = eval(f'course.Расписание{n}')
                            group.opened = True if eval(f'course.Статус{n}') == 'Набор открыт' else False
                            existing_course.groups.append(group)
                db_session.add(existing_course)
                db_session.commit()
                print(f'{existing_course.name} updated')
            else:
                new_course = Course(
                    name=course.Программа.upper(),
                    focus=course.Направленность.upper(),
                    teachers=course.Педагоги.split(", "),
                    table_id=course.id
                )
                print(f'Создаю курс {new_course.table_id}')
                if type(course.Возраст) != float:
                    if '-' in course.Возраст:
                        new_course.age_from = course.Возраст.split("-")[0]
                        new_course.age_to = course.Возраст.split("-")[1]
                    elif '+' in course.Возраст:
                        new_course.age_from = course.Возраст[:-1]
                    else:
                        new_course.age_from = course.Возраст
                if type(course.Направление) != float:
                    new_course.direction = course.Направление.upper()
                if type(course.Форма) != float:
                    if course.Форма == 'Бюджет':
                        new_course.free = True
                    elif course.Форма == 'Платно':
                        new_course.free = False
                    if course.Форма == 'Сертификат':
                        new_course.certificate = True
                    else:
                        new_course.certificate = False
                if type(course.Описание) != float:
                    new_course.description = course.Описание
                if type(course.Код) != float:
                    new_course.code = int(course.Код)
                if type(course.Площадка) != float:
                    new_course.area = course.Площадка.upper()
                for n in range(1, 7):
                    group = Group()
                    if type(eval(f'course.Расписание{n}')) != float:
                        group.number = n
                        group.schedule = eval(f'course.Расписание{n}')
                        group.opened = True if eval(f'course.Статус{n}') == 'Набор открыт' else False
                        new_course.groups.append(group)
                db_session.add(new_course)
                db_session.commit()
                print(f'{new_course.name} created')
