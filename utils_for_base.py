from db import db_session
from db.models import Group, Course, Record, records_groups, records_courses
from sqlalchemy import and_, update
from sqlalchemy.dialects.postgresql import Any

from utilities import get_all_records


def find_and_delete_record(db_sess):
    print('Введите <Фамилию Имя> ребёнка\n')
    surname, name = input().split()
    recs = db_sess.query(Record).filter(and_(Record.child_surname == surname,
                                             Record.child_name == name)).all()
    if not recs:
        print('Такая запись не найдена')
        return
    for rec in recs:
        print('-------------------------------------------------------------------------------------------------------')
        print(f'№{rec.id} {surname} {name} {rec.child_patronymic} {rec.child_birthday}')
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
        groups_num_to_delete = list(map(int, input('Введите id групп из которой необходимо удалить ребёнка через пробел\n').split()))
        print(f'Удаляем запись {id_to_delete} из групп {groups_num_to_delete}? (Y/N)\n')
        answer = input().lower()
        while answer not in 'yn':
            answer = input('Не понял, удаляем или нет? (Y/N)\n').lower()
        if answer == 'n':
            return
        else:
            for g in groups_num_to_delete:
                course_to_delete = db_sess.query(Course).select_from(Group).join(Course.groups).filter(
                    Group.id == g).first()
                db_sess.execute(f'delete from records_groups_23 where record_id = {id_to_delete} and group_id = {g}')
                db_sess.execute(f'delete from records_courses_23 where record_id = {id_to_delete} and course_id = {course_to_delete.id}')
            db_sess.commit()
            db_sess.close()
            print('Удалено')
    else:
        return


def find_course_and_group(db_sess):
    print('Введите примерное название программы\n')
    answer = input().upper()
    courses = db_sess.query(Course).filter(Course.name.contains(answer)).all()
    if not courses:
        print('Ничего не найдено')
        return
    for course in courses:
        print('-------------------------------------------------------------------------------------------------------')
        groups = db_sess.query(Group).filter(Group.course_id == course.id).all()
        print(f'{course.teachers} - {course.name}')
        for group in groups:
            print(f'ID{group.id} Группа № {group.number} - {group.schedule} / {"открыта" if group.opened else "закрыта"}')
        print('-------------------------------------------------------------------------------------------------------')
    group_to_work = list(map(int, (input('Какие группы открыть?(ID)\n').split())))
    for group_num in group_to_work:
        group = db_sess.query(Group).filter(Group.id == group_num).first()
        group.opened = True
        db_sess.add(group)
    db_sess.commit()
    db_sess.close()
    print('Done')
    return


def run():
    db_sess = db_session.create_db_session()
    answer = ''
    while answer != 'exit':
        find_course_and_group(db_sess)


run()

