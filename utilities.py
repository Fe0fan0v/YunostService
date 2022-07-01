from sqlalchemy import and_
from db.models import Course, Registration
from flask import request
from db.models import Record


def show_courses(db_sess):
    sort_type = request.args.get('sort_type')
    courses = db_sess.query(Course).all()
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
