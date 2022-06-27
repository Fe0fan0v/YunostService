import datetime
import json

from flask import Flask, render_template, request, redirect, url_for, send_file
from flask_cors import CORS

from db.models import Course, Record, Association, Registration
from forms import RegisterChild, AdminEnter, SearchForm, OldRegister, CourseForm, RedactCourse
from utilities import show_courses, get_filter_criteria
from sendmail import send
from env import admin_password
from sqlalchemy import and_
from db.db_session import db_session, init_db
from api.api import api_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super_secret_key'
init_db()
CORS(app)
app.register_blueprint(api_bp)


@app.route('/', methods=['GET', 'POST'])
def main_page():
    return redirect('/enroll')
    # return render_template('index.html')


@app.route('/enroll')
def enroll():
    args = request.args.to_dict()
    courses, areas, directions, nav_areas = show_courses(db_session)
    if not args:
        return render_template('enroll.html', title='Запись', courses=courses, areas=areas, directions=directions,
                               nav_areas=nav_areas)
    elif 'message_type' in args.keys():
        return render_template('enroll.html', title='Запись', courses=courses, areas=areas, directions=directions,
                               nav_areas=nav_areas, message_type=args['message_type'],
                               message=args['message'])
    else:
        return render_template('enroll.html', title='Запись', courses=courses, areas=areas, directions=directions,
                               nav_areas=nav_areas)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegisterChild()
    args = request.args.to_dict()
    course_id, group_number = args['course'], args['group']
    course = db_session.query(Course).get(course_id)
    count_records = len(db_session.query(Association).filter(
        and_(Association.course_id == course_id, Association.group == group_number)).all())
    if request.method == 'POST':
        data = request.form
        child_birthday = datetime.datetime.fromisoformat(data['child_birthday']).date()
        age = (datetime.date.today() - child_birthday).days // 365
        if not course.age_from <= age <= course.age_to:
            return render_template('registration.html', course=course, form=form, group=group_number,
                                   count_records=count_records, message='Курс не подходит Вам по возрасту')
        registered = db_session.query(Record).filter(
            and_(
                Record.child_name == data['child_name'].strip().capitalize(),
                Record.child_surname == data['child_surname'].strip().capitalize(),
                Record.child_patronymic == data['child_patronymic'].strip().capitalize(),
                Record.child_birthday == child_birthday
            )
        ).first()
        if registered:
            if any(map(lambda ass: ass.course_id == course_id, registered.courses)):
                return redirect(url_for('enroll', message_type='danger', message='Вы уже записаны в это объединение!'))
            elif len(registered.courses) >= 3:
                return redirect(url_for('enroll', message_type='danger',
                                        message='Превышен лимит записей.'))
            else:
                assoc = Association()
                assoc.group = data['group']
                assoc.course = course
                assoc.record = registered
                db_session.add(assoc)
                db_session.commit()
                send(registered.parent_email, 'Запись в ДДТ Юность', course.name, data['group'])
                return redirect(
                    url_for('enroll', message_type='success', message="Ваша запись успешно зарегистрирована"))

        else:
            record = Record(child_name=data['child_name'].strip().capitalize(),
                            child_surname=data['child_surname'].strip().capitalize(),
                            child_patronymic=data['child_patronymic'].strip().capitalize(),
                            child_birthday=child_birthday,
                            educational_institution=data['educational_institution'],
                            edu_class=data['edu_class'],
                            health=data['health'],
                            child_phone=data['child_phone'],
                            child_email=data['child_email'],
                            child_residence=data['child_residence'],
                            parent_name=data['parent_name'],
                            parent_surname=data['parent_surname'],
                            parent_patronymic=data['parent_patronymic'],
                            parent_birthday=datetime.datetime.fromisoformat(data['parent_birthday']).date(),
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
                            second_parent_phone=data['second_parent_phone'] if data[
                                'second_parent_phone'] else None)
            assoc = Association()
            assoc.group = data['group']
            assoc.course = course
            assoc.record = record
            db_session.add(assoc)
            db_session.add(record)
            db_session.commit()
            send(record.parent_email, 'Запись в ДДТ Юность', course.name, data['group'])
            return redirect(
                url_for('enroll', message_type='success', message="Ваша запись успешно зарегистрирована"))
    return render_template('registration.html', course=course, form=form, group=group_number,
                           count_records=count_records)


@app.route('/admin', methods=['GET', 'POST'])  # панель администратора
def admin_panel():
    form = AdminEnter()
    search_form = SearchForm()
    if search_form.validate_on_submit():
        records = get_filter_criteria(db_session, search_form.area_search.data, search_form.direction_search.data,
                                      search_form.cube.data, search_form.success.data)
        if not records:
            return render_template('admin_panel.html', message='Ничего не найдено', search_form=search_form)
        else:
            children = [child.to_dict() for child in records]
            for child in children:
                child['child_birthday'] = (datetime.date.today() - datetime.date.fromisoformat(
                    child['child_birthday'])).days // 365
            return render_template('admin_panel.html', children=children, search_form=search_form)
    if form.validate_on_submit():
        if request.form.get('password') == admin_password:
            children = [child.to_dict() for child in db_session.query(Record).all()]
            for child in children:
                child['child_birthday'] = (datetime.date.today() - datetime.date.fromisoformat(
                    child['child_birthday'])).days // 365
            return render_template('admin_panel.html', children=children, search_form=search_form)
    return render_template('admin.html', form=form)


@app.route('/download/<filename>')
def return_files(filename):
    file_path = filename
    return send_file(file_path, as_attachment=True, attachment_filename='')


@app.route('/old')
def first_old():
    reg = db_session.query(Registration).first()
    return redirect(f'/old/{reg.id}')


@app.route('/old/<id>')
def current_old(id):
    reg = db_session.query(Registration).get(id)
    form = OldRegister(
        child_name=reg.child_name,
        child_surname=reg.child_surname,
        child_patronymic=reg.child_patronymic,
        child_birthday=reg.child_birthday,
        educational_institution=reg.educational_institution,
        edu_class=reg.edu_class,
        health=reg.health,
        child_phone=reg.child_phone,
        child_email=reg.child_email,
        child_residence=reg.child_residence,
        parent_name=reg.parent_name,
        parent_surname=reg.parent_surname,
        parent_patronymic=reg.parent_patronymic,
        parent_birthday=reg.parent_birthday,
        parent_residence=reg.parent_residence,
        parent_work=reg.parent_work,
        parent_phone=reg.parent_phone,
        parent_email=reg.parent_email,
        full_family=reg.full_family,
        large_family=reg.large_family,
        without_parents=reg.without_parents,
        police_record=reg.police_record,
        resident=reg.resident,
        second_parent_fio=reg.second_parent_phone,
        second_parent_phone=reg.second_parent_phone
    )
    # courses = db_session.query(Course).all()  # todo: выводить новые курсы и соответствующие группы
    course_form = CourseForm()
    for course in reg.courses:
        subform = form.courses.append_entry(course_form)
        subform.old_name.data = course
        # subform.old_group.data = reg.courses[course]
    return render_template('manual.html', form=form)


@app.route('/to_redact', methods=['GET', 'POST'])
def redact():
    form = RedactCourse()
    courses, areas, directions, nav_areas = show_courses(db_session)
    course = db_session.query(Course).filter(Course.id == request.args['course']).first()
    form.area.choices = [(i, area) for i, area in enumerate(nav_areas)]
    form.area.default = nav_areas.index(course.area)
    form.focus.choices = [(i, focus) for i, focus in enumerate(directions.keys())]
    form.focus.default = list(directions.keys()).index(course.focus)
    form.direction.choices = [(i, direction) for i, direction in enumerate(directions[course.focus])]
    form.direction.default = directions[course.focus].index(course.direction)
    form.code.default = course.code
    form.process()
    if request.method == 'POST':
        data = request.form.to_dict()
        course.name = data['name'].strip()
        course.area = form.area.choices[int(data['area'])][1]
        course.focus = form.focus.choices[int(data['focus'])][1]
        course.direction = form.direction.choices[int(data['direction'])][1]
        course.teachers = data['teachers'].strip().split(', ')
        course.description = data['description'].strip()
        course.age_from = data['age_from']
        course.age_to = data['age_to']
        course.free = True if data['free'] == 'y' else False
        course.code = data['code']
        db_session.add(course)
        db_session.commit()
        return redirect('/redact')
    return render_template('redact.html', course=course, form=form,
                           directions=directions, ensure_ascii=False)


@app.route('/redact')
def courses_to_redact():
    courses, areas, directions, nav_areas = show_courses(db_session)
    return render_template('courses_to_redact.html', courses=courses, areas=areas, directions=directions,
                           nav_areas=nav_areas)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
