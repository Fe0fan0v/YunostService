import datetime

from flask import Flask, render_template, request, redirect, jsonify
from db import db_session
from db.models import Course, Registration
from forms import NewCourse, RegisterForm, RegisterChild
import urllib.parse
from showing import show_courses
from pprint import pprint

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super_secret_key'
db_session.global_init()


@app.route('/', methods=['GET', 'POST'])
def main_page():
    return render_template('index.html')


@app.route('/enroll', methods=['GET', 'POST'])
def enroll():
    form = RegisterChild()
    db_sess = db_session.create_session()
    courses, areas, directions, nav_areas = show_courses(db_sess)
    if request.method == 'POST':
        data = request.form
        record = Registration(child_name=data['child_name'],
                              child_surname=data['child_surname'],
                              child_patronymic=data['child_patronymic'],
                              child_birthday=datetime.date(int(data['child_birthday'].split('.')[-1]),
                                                           int(data['child_birthday'].split('.')[1]),
                                                           int(data['child_birthday'].split('.')[0])),
                              educational_institution=data['educational_institution'],
                              edu_class=data['edu_class'],
                              health=data['health'],
                              child_phone=data['child_phone'],
                              child_email=data['child_email'],
                              child_residence=data['child_residence'],
                              parent_name=data['parent_name'],
                              parent_surname=data['parent_surname'],
                              parent_patronymic=data['parent_patronymic'],
                              parent_birthday=datetime.date(int(data['parent_birthday'].split('.')[-1]),
                                                            int(data['parent_birthday'].split('.')[1]),
                                                            int(data['parent_birthday'].split('.')[0])),
                              parent_residence=data['parent_residence'],
                              parent_work=data['parent_work'],
                              parent_phone=data['parent_phone'],
                              parent_email=data['parent_email'],
                              full_family=True if data['full_family'] == 'Полная семья' else False,
                              large_family=True if data['large_family'] == 'Многодетная семья' else False,
                              without_parents=False if data['without_parents'] == 'Нет' else True,
                              police_record=False if data['police_record'] == 'Нет' else True,
                              resident=False if data['resident'] == 'Нет' else True,
                              second_parent_fio=data['second_parent_fio'] if data['second_parent_fio'] else None,
                              second_parent_phone=data['second_parent_phone'] if data['second_parent_phone'] else None,
                              courses={data['course_name']: data['group']}
                              )
        registered = db_sess.query(Registration).filter((Registration.child_name == record.child_name) and (
                Registration.child_surname == record.child_surname) and (
                                                                Registration.child_patronymic == record.child_patronymic)).first()
        if registered:
            if any(map(lambda x: list(record.courses.keys())[0] in x, list(registered.courses.keys()))):
                return render_template('enroll.html', title='Запись', courses=courses, areas=areas,
                                       directions=directions,
                                       nav_areas=nav_areas, form=form,
                                       message_type='danger',
                                       message='Вы уже записаны в это объединение!')
            else:
                registered.courses[list(record.courses.keys())[0]] = list(record.courses.values())[0]   # todo: добавление ещё одного курса в запись (не работает)
                db_sess.commit()
                print('this')
                return render_template('enroll.html', title='Запись', courses=courses, areas=areas,
                                       directions=directions,
                                       nav_areas=nav_areas, form=form, message_type='success',
                                       message='Вы успешно записаны!')
        else:
            db_sess.add(record)
            db_sess.commit()
            return render_template('enroll.html', title='Запись', courses=courses, areas=areas, directions=directions,
                                   nav_areas=nav_areas, form=form, message_type='success',
                                   message='Вы успешно записаны!')
    return render_template('enroll.html', title='Запись', courses=courses, areas=areas, directions=directions,
                           nav_areas=nav_areas, form=form)


@app.route('/admin')  # панель администратора
def admin_panel():
    db_sess = db_session.create_session()
    courses, areas, directions, nav_areas = show_courses(db_sess)
    return render_template('admin.html', title='Панель администратора', courses=courses, areas=areas,
                           directions=directions, nav_areas=nav_areas)


@app.route('/add_course', methods=['GET', 'POST'])  # добавление нового курса
def add_course():
    form = NewCourse()
    if request.method == 'POST':
        db_sess = db_session.create_session()
        data = request.form
        form_data = urllib.parse.parse_qs(data['form_data'])
        lessons_data = eval(data['lessons_data'])
        new_course = Course(name=form_data['name'][0],
                            direction=form_data['direction'][0],
                            area=form_data['area'][0],
                            teacher=form_data['teacher'][0],
                            age_from=int(form_data['age_from'][0]),
                            age_to=int(form_data['age_to'][0]),
                            schedule=lessons_data,
                            description=form_data['description'][0])
        db_sess.add(new_course)
        db_sess.commit()
        return redirect('/admin')
    return render_template('add_course.html', title='Добавить новое объединение', form=form)


@app.route('/delete_course/<_id>')
def delete_course(_id):
    db_sess = db_session.create_session()
    course = db_sess.query(Course).filter(Course.id == _id).first()
    db_sess.delete(course)
    db_sess.commit()
    return redirect('/admin')


@app.route('/redact_course/<_id>', methods=['GET', 'POST'])
def redact_course(_id):
    form = NewCourse()
    db_sess = db_session.create_session()
    course = db_sess.query(Course).filter(Course.id == _id).first()
    if request.method == 'POST':  # todo: удаление и добавление групп
        data = request.form.to_dict()
        print(data)
    return render_template('redact_course.html', course=course, form=form, title='Редактирование объединения')


if __name__ == '__main__':
    db_session.global_init()
    app.run()
