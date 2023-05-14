import numpy
from sqlalchemy import and_

from db.db_session import create_db_session
from db.models import Course, Group, Record
from flask import request
import pandas
import requests
from urllib.parse import urlencode


def show_courses(db_sess, addit=False):
    sort_type = request.args.get('sort_type')
    try:
        if not addit:
            courses = db_sess.query(Course).filter(Course.counter == 0).all()
        else:
            courses = db_sess.query(Course).filter(Course.counter == 1).all()
    except:
        db_sess.rollback()
    nav_areas = list(set(course.area for course in courses))
    directions = {}
    for course in courses:
        directions.setdefault(course.focus, set()).add(course.direction)
    for focus in directions:
        directions[focus] = sorted(directions[focus])
    if not sort_type:
        pass
    elif sort_type.split('_')[0] != 'age':
        sort_type, sort_data = sort_type.split('_')
        if sort_type == 'cube':
            courses = db_sess.query(Course).filter(Course.code == 1).all()
        elif sort_type == 'success':
            courses = db_sess.query(Course).filter(Course.code == 2).all()
        else:
            courses = eval(f'db_sess.query(Course).filter(Course.{sort_type} == "{sort_data}").all()')
    else:
        age = int(sort_type.split('_')[1])
        courses = list(filter(lambda x: x.age_from <= age <= x.age_to, courses))
    areas = {}
    for course in courses:
        if course.area in areas:
            if course.direction not in areas[course.area]:
                areas[course.area].append(course.direction)
            else:
                continue
        else:
            areas[course.area] = [course.direction]
    db_sess.close()
    return courses, areas, directions, nav_areas


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
    for i, course in enumerate(data.itertuples()):
        current_course = Course(
            name=course.Название.upper(),
            age_from=course.Возраст.split("-")[0],
            age_to=course.Возраст.split("-")[1],
            focus=course.Направленность.upper(),
            direction=course.Направление.upper(),
            certificate=True if course.Сeртификат == "Да" else False,
            area=course.Площадка.upper(),
            teachers=course.Педагоги.split(", "),
            description=course.Описание,
            free=True if course.Форма == 'Бюджет' else False,
            code=int(course.Код)
        )
        for n in range(1, 7):
            group = Group()
            if type(eval(f'course.Расписание{n}')) != float:
                group.number = n
                group.schedule = eval(f'course.Расписание{n}')
                group.opened = True if eval(f'course.Статус{n}') == 'Набор открыт' else False
                current_course.groups.append(group)
        db_session.add(current_course)
        db_session.commit()
