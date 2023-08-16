from db import db_session
from db.models import Group, Course, Record, records_groups, records_courses
from sqlalchemy import and_

from utilities import get_all_records


def get_groups_and_courses():
    db_sess = db_session.create_db_session()
    print('Введите <Фамилию Имя> ребёнка\n')
    surname, name = input().split()
    recs = db_sess.query(Record).filter(and_(Record.child_surname == surname,
                                             Record.child_name == name)).all()
    if not recs:
        print('Такая запись не найдена')
        return
    for rec in recs:
        print('-------------------------------------------------------------------------------------------------------')
        print(f'№{rec.id} {surname} {name}')
        result = {}
        courses = db_sess.query(Course).select_from(Record).join(Course.records).filter(
            and_(Record.child_surname == rec.child_surname,
                 Record.child_name == rec.child_name)).all()
        groups = db_sess.query(Group).select_from(Record).join(Group.records).filter(
            and_(Record.child_surname == rec.child_surname,
                 Record.child_name == rec.child_name)).all()
        for course in courses:
            result[f'{course.id} {course.name}'] = []
            for group in groups:
                if group in course.groups:
                    result[f'{course.id} {course.name}'].append(group.id)
        for course in result:
            print(f'Курс {course} - группа {result[course]}')
        print('-------------------------------------------------------------------------------------------------------')
    print('Что делаем дальше? (D - удалить, другое - выйти)')
    todo = input().lower()
    if todo == 'd':
        id_to_delete = int(input('Введите id записи ребёнка для удаления\n'))
        group_num_to_delete = int(input('Введите id группы из которой необходимо удалить ребёнка\n'))
        print(f'Удаляем запись {id_to_delete} из группы {group_num_to_delete}? (Y/N)\n')
        answer = input().lower()
        while answer != 'y':
            if answer == 'n':
                return
            elif answer == 'y':
                course_to_delete = db_sess.query(Group).filter(Group.id == group_num_to_delete).first()
                db_sess.query(records_groups).filter(and_(records_groups.record_id == id_to_delete,
                                                          records_groups.group_id == group_num_to_delete)).delete()
                db_sess.query(records_courses).filter(and_(records_courses.record_id == id_to_delete,
                                                           records_groups.course_id == course_to_delete.course_id)).delete()

            else:
                answer = input('Не понял, удаляем или нет? (Y/N)\n').lower()
    else:
        return


get_groups_and_courses()
