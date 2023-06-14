import datetime
from pprint import pprint

from flask import Flask, render_template, request, redirect, send_file, url_for
from flask_cors import CORS

from db.models import Course, Record, Group
from forms import RegisterChild, AdminEnter
from utilities import show_courses, get_filter_criteria
from sendmail import send
from env import admin_password
from sqlalchemy import and_
from db.db_session import create_db_session, init_db
# from api.api import api_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super_secret_key'
init_db()
CORS(app)
# app.register_blueprint(api_bp)

DIRECTIONS = {'Художественная': ['ИЗОБРАЗИТЕЛЬНОЕ ИСКУССТВО', 'ВОКАЛ', 'ХОРЕОГРАФИЯ', 'ТЕАТР', 'ЦИРК', 'ДЕКОРАТИВНО-ПРИКЛАДНОЕ ТВОРЧЕСТВО (ВАЛЯНИЕ ИЗ ШЕРСТИ, БИСЕРОПЛЕТЕНИЕ, ТЕКСТИЛЬНАЯ КУКЛА И ДР.)', 'ПРОЕКТИРОВАНИЕ СОВРЕМЕННОЙ ОДЕЖДЫ', 'МУЗЫКАЛЬНАЯ ДЕЯТЕЛЬНОСТЬ'],
              'Физкультурно-спортивная': ['СПОРТ', 'ШАХМАТЫ'],
              'Социально-гуманитарная': ['ЖУРНАЛИСТИКА', 'ПСИХОЛОГИЯ', 'АНГЛИЙСКИЙ ЯЗЫК', 'ПОДГОТОВКА К ШКОЛЕ', 'МУЛЬТИМЕДИА', 'МЕДИА', 'ФИНАНСОВАЯ ГРАМОТНОСТЬ', 'ОБЩЕСТВОЗНАНИЕ', 'ПРОФЕССИОНАЛЬНОЕ САМООПРЕДЕЛЕНИЕ.', 'СКОРОЧТЕНИЕ, МНЕМОТЕХНИКА, УСТНЫЙ СЧЁТ.'],
              'Техническая': [' КОНСТРУИРОВАНИЕ, МОДЕЛИРОВАНИЕ', 'IT (ПРОГРАММИРОВАНИЕ, РОБОТОТЕХНИКА, ТЕХНИЧЕСКИЙ АНГЛИЙСКИЙ И ДР.)', 'СТОЛЯРНОЕ ДЕЛО', 'РЕЗЬБА ПО ДЕРЕВУ', 'ЭЛЕКТРОНИКА', 'БУМАГОПЛАСТИКА'],
              'Естественно-научная': ['ЕСТЕСТВЕННЫЕ НАУКИ (ХИМИЯ, БИОЛОГИЯ, АСТРОНОМИЯ, ГЕОЛОГИЯ)'],
              'Туристско-краеведческая': ['ЕСТЕСТВЕННЫЕ НАУКИ']}


@app.route('/')
def enroll():
    args = request.args.to_dict()
    db_session = create_db_session()
    courses, areas, directions = show_courses(db_session)
    if not args:
        db_session.close()
        return render_template('enroll.html', title='Запись', courses=courses, areas=areas, directions=DIRECTIONS)
    elif 'message_type' in args.keys():
        db_session.close()
        return render_template('enroll.html', title='Запись', courses=courses, areas=areas, directions=DIRECTIONS, message_type=args['message_type'],
                               message=args['message'])
    if 'overflow' in args.keys():
        return render_template('enroll.html', title='Запись', courses=courses, areas=areas, directions=DIRECTIONS,
                               message_type=args['message_type'],
                               message=args['message'], overflow=True)
    else:
        db_session.close()
        return render_template('enroll.html', title='Запись', courses=courses, areas=areas, directions=DIRECTIONS)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegisterChild()
    args = request.args.to_dict()
    course_id, group_id = args['course'], args['group']
    db_session = create_db_session()
    course = db_session.query(Course).get(course_id)
    group = db_session.query(Group).get(group_id)
    count_records = len(group.records)
    if request.method == 'POST':
        data = request.form
        child_birthday = datetime.datetime.fromisoformat(data['child_birthday']).date()
        age = (datetime.date.today() - child_birthday).days // 365
        if not course.age_from - 2 <= age <= course.age_to + 2:
            db_session.close()
            return render_template('registration.html', course=course, form=form, group=group,
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
            if course in registered.courses:
                return redirect(url_for('enroll', message_type='danger', message='Вы уже записаны в это объединение!'))
            elif len(registered.courses) >= 3:
                return redirect(url_for('enroll', message_type='danger',
                                        message='Вы уже записаны в три объединения.'))
            elif course.code == 1 and any(map(lambda cour: cour.code == 1, registered.courses)):
                return redirect(url_for('enroll', message_type='danger',
                                        message='Вы уже записаны в IT-Cube.'))
            elif course.code == 2 and any(map(lambda cour: cour.code == 2, registered.courses)):
                return redirect(url_for('enroll', message_type='danger',
                                        message='Вы уже записаны в Успех каждого ребёнка.'))
            else:
                registered.courses.append(course)
                registered.groups.append(group)
                db_session.add(registered)
                if course.certificate:
                    registered.certificate_number = data['certificate']
                db_session.commit()
                send(registered.parent_email, 'Запись в ДДТ Юность', course.name, data['group'])
                db_session.close()
                if count_records > 15:
                    return redirect(
                        url_for('enroll', message_type='success',
                                message="Ваша запись успешно зарегистрирована", overflow=True))
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
                            snils=data['snils'],
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
            record.courses.append(course)
            record.groups.append(group)
            db_session.add(record)
            db_session.commit()
            send(record.parent_email, 'Запись в ДДТ Юность', course.name, data['group'])
            db_session.close()
            if count_records > 15:
                return redirect(
                    url_for('enroll', message_type='success',
                            message="Ваша запись успешно зарегистрирована", overflow=True))
            return redirect(
                url_for('enroll', message_type='success', message="Ваша запись успешно зарегистрирована"))
    db_session.close()
    return render_template('registration.html', course=course, form=form, group=group,
                           count_records=count_records)


@app.route('/admin', methods=['GET', 'POST'])  # панель администратора
def admin_panel():
    form = AdminEnter()
    db_session = create_db_session()
    if form.validate_on_submit():
        if request.form.get('password') == admin_password:
            records = db_session.query(Record).all()
            courses, areas, directions = show_courses(db_session)
            teachers = list(set([course.teachers[0] for course in courses]))
            for record in records:
                record.child_birthday = (datetime.date.today() - record.child_birthday).days // 365
            # records = list(map(lambda x: x.to_dict(), records))
            db_session.close()
            return render_template('admin_panel.html', children=records, teachers=teachers, courses=courses,
                                   areas=areas, directions=DIRECTIONS)
    db_session.close()
    return render_template('admin.html', form=form)


@app.route('/admin/group/<num>')
def get_group(num):
    db_sess = create_db_session()
    records = db_sess.query(Record).select_from(Group).join(Record.groups).filter(Group.id == num).all()
    for record in records:
        record.child_birthday = (datetime.date.today() - record.child_birthday).days // 365
    return render_template('show_records.html', records=enumerate(records))


@app.route('/download/<filename>')
def return_files(filename):
    file_path = filename
    return send_file(file_path, as_attachment=True, attachment_filename='')


@app.route('/report')
def report():
    from db.tools.report import get_report
    filename = 'report.xlsx'
    get_report(filename)
    return send_file(filename, as_attachment=True, attachment_filename='report.xlsx')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
