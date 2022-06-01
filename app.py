import datetime

from flask import Flask, render_template, request, redirect, url_for, send_file
from db import db_session
from db.models import Course, Registration
from forms import RegisterChild, AdminEnter
import urllib.parse
from showing import show_courses
from sqlalchemy.orm.attributes import flag_modified
from sendmail import send
from env import admin_password

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super_secret_key'
db_session.global_init()


@app.route('/', methods=['GET', 'POST'])
def main_page():
    return redirect('/enroll')
    # return render_template('index.html')


@app.route('/enroll', methods=['GET', 'POST'])
def enroll():
    form = RegisterChild()
    db_sess = db_session.create_session()
    courses, areas, directions, nav_areas = show_courses(db_sess)
    args = request.args.to_dict()
    if request.method == 'POST':
        data = request.form
        registered = db_sess.query(Registration).filter((Registration.child_name == data['child_name']) and (
                Registration.child_surname == data['child_surname']) and (
                                                                Registration.child_patronymic == data[
                                                            'child_patronymic'])).first()
        if registered:
            if any(map(lambda x: data['course_name'] in x, list(registered.courses.keys()))):
                return redirect(url_for('enroll', message_type='danger', message='Вы уже записаны в это объединение!'))
            else:
                registered.courses[data['course_name']] = data['group']
                db_sess.add(registered)
                flag_modified(registered, 'courses')
                db_sess.commit()
                send(registered.parent_email, 'Запись в ДДТ Юность')
                return redirect(
                    url_for('enroll', message_type='success', message="Ваша запись успешно зарегистрирована"))
        else:
            record = Registration(child_name=data['child_name'],
                                  child_surname=data['child_surname'],
                                  child_patronymic=data['child_patronymic'],
                                  child_birthday=datetime.date(int(data['child_birthday'].split('-')[0]),
                                                               int(data['child_birthday'].split('-')[1]),
                                                               int(data['child_birthday'].split('-')[2])),
                                  educational_institution=data['educational_institution'],
                                  edu_class=data['edu_class'],
                                  health=data['health'],
                                  child_phone=data['child_phone'],
                                  child_email=data['child_email'],
                                  child_residence=data['child_residence'],
                                  parent_name=data['parent_name'],
                                  parent_surname=data['parent_surname'],
                                  parent_patronymic=data['parent_patronymic'],
                                  parent_birthday=datetime.date(int(data['parent_birthday'].split('-')[0]),
                                                                int(data['parent_birthday'].split('-')[1]),
                                                                int(data['parent_birthday'].split('-')[2])),
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
                                      'second_parent_phone'] else None,
                                  courses={data['course_name']: data['group']}
                                  )
            course = db_sess.query(Course).filter(Course.name == data['course_name']).first()
            course.counter += 1
            db_sess.add(record)
            db_sess.commit()
            send(record.parent_email, 'Запись в ДДТ Юность')
            return redirect(
                url_for('enroll', message_type='success', message="Ваша запись успешно зарегистрирована"))
    if not args:
        return render_template('enroll.html', title='Запись', courses=courses, areas=areas, directions=directions,
                               nav_areas=nav_areas, form=form)
    elif 'message_type' in args.keys():
        return render_template('enroll.html', title='Запись', courses=courses, areas=areas, directions=directions,
                               nav_areas=nav_areas, form=form, message_type=args['message_type'],
                               message=args['message'])
    else:
        return render_template('enroll.html', title='Запись', courses=courses, areas=areas, directions=directions,
                               nav_areas=nav_areas, form=form)


@app.route('/admin', methods=['GET', 'POST'])  # панель администратора
def admin_panel():
    form = AdminEnter()
    if form.validate_on_submit():
        if request.form.get('password') == admin_password:
            db_sess = db_session.create_session()
            courses, areas, directions, nav_areas = show_courses(db_sess)
            children = db_sess.query(Registration).all()
            return render_template('admin_panel.html', courses=courses, areas=areas,
                                   directions=directions, nav_areas=nav_areas, children=children)
    return render_template('admin.html', form=form)


@app.route('/download/<filename>')
def return_files(filename):
    file_path = filename
    return send_file(file_path, as_attachment=True, attachment_filename='')


if __name__ == '__main__':
    db_session.global_init()
    app.run(host='0.0.0.0')
