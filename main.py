import datetime

from flask import Flask, render_template, request, redirect, url_for, send_file
from db.models import Course, Record, Association
from forms import RegisterChild, AdminEnter
from showing import show_courses
from sendmail import send
from env import admin_password
from sqlalchemy import and_
from db.db_session import db_session, init_db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super_secret_key'
init_db()


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
    if request.method == 'POST':
        data = request.form
        child_birthday = datetime.datetime.fromisoformat(data['child_birthday']).date()
        age = (datetime.date.today() - child_birthday).days // 365
        if not course.age_from <= age <= course.age_to:
            return render_template('registration.html', course=course, form=form, group=group_number,
                                   message='Курс не подходит Вам по возрасту')
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
    return render_template('registration.html', course=course, form=form, group=group_number)


@app.route('/admin', methods=['GET', 'POST'])  # панель администратора
def admin_panel():
    form = AdminEnter()
    if form.validate_on_submit():
        if request.form.get('password') == admin_password:
            courses, areas, directions, nav_areas = show_courses(db_session)
            children = [row.__dict__ for row in db_session.query(Registration).all()]
            for child in children:
                del child['_sa_instance_state']
                del child['police_record']
                del child['resident']
                del child['full_family']
                del child['large_family']
                del child['without_parents']
                del child['second_parent_fio']
                del child['second_parent_phone']
                del child['id']
                child['parent_birthday'] = child['parent_birthday'].strftime("%d.%m.%Y")
                child['child_birthday'] = (datetime.date.today() - child['child_birthday']).days // 365
            return render_template('admin_panel.html', children=children, courses=courses, areas=areas,
                                   directions=directions, nav_areas=nav_areas)
    return render_template('admin.html', form=form)


@app.route('/download/<filename>')
def return_files(filename):
    file_path = filename
    return send_file(file_path, as_attachment=True, attachment_filename='')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
