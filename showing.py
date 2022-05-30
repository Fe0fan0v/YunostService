from db.models import Course
from flask import request


def show_courses(db_sess):
    sort_type = request.args.get('sort_type')
    courses = db_sess.query(Course).all()
    nav_areas = list(set(course.area for course in courses))
    directions = list(set(course.direction for course in courses))
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
