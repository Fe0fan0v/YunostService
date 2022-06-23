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
        courses = list(filter(lambda x: x.age_from <= age < x.age_to, courses))
    areas = {}
    for course in courses:
        if course.area in areas:
            if course.direction not in areas[course.area]:
                areas[course.area].append(course.direction)
            else:
                continue
        else:
            areas[course.area] = [course.direction]
    return courses, areas, directions, nav_areas


def get_filter_criteria(db_sess, area, direction, cube, success):
    try:
        area = None if area == 'ВСЕ' else area
        direction = None if direction == 'ВСЕ' else direction
        if cube:
            code = 1
        elif success:
            code = 2
        else:
            code = -1
        if direction and area:
            records = db_sess.query(Record).join("courses", "course").filter(and_(
                Course.area == area,
                Course.direction == direction,
            )).all()
        elif direction and not area:
            records = db_sess.query(Record).join("courses", "course").filter(and_(
                Course.direction == direction,
            )).all()
        elif area and not direction:
            records = db_sess.query(Record).join("courses", "course").filter(and_(
                Course.area == area,
            )).all()
        else:
            records = db_sess.query(Record).join("courses", "course").filter(and_(
                Course.code == code
            )).all()
        return records
    except:
        return None