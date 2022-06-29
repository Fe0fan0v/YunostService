import datetime

from db.db_session import init_db, db_session
from db.models import Course, Registration, Record, Association


init_db()
now = datetime.date.today()

for reg in db_session.query(Registration).all():
    reg_data = reg.as_dict()
    courses_dict = reg_data.pop('courses')
    age = (now - reg_data['child_birthday']).days // 365
    rec = Record(**reg_data)
    for c, g in courses_dict.items():
        found_courses = db_session.query(Course).filter(Course.name == c).all()
        comments = []
        if len(found_courses) > 1:
            if all(not course.age_from <= age <= course.age_to for course in found_courses):
                comments.append('возраст не подходит')
            else:
                found_courses = list(filter(lambda c: c.age_from <= age <= c.age_to, found_courses))
            if sum(g in course.schedule for course in found_courses) > 1:
                comments.append('уточнить группу')
        assoc = Association()
        assoc.group = g
        assoc.comment = ', '.join(comments)
        assoc.course = found_courses[0]
        assoc.record = rec
        db_session.add(assoc)
    db_session.add(rec)
db_session.commit()
