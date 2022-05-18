from flask import Flask, render_template, request, redirect, jsonify
from db import db_session
from db.models import Course
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


@app.route('/enroll', methods=['GET', 'POST'])  # todo: страница записи ребёнка
def enroll():
    form = RegisterChild()
    db_sess = db_session.create_session()
    courses, areas, directions, nav_areas = show_courses(db_sess)  # todo: раздельная сортировка
    if request.method == 'POST':
        data = request
        print(data)
        form_data = urllib.parse.parse_qs(data['form_data'])
        lessons_data = eval(data['lessons_data'])
        print(form_data)
        print(lessons_data)
        return jsonify({'msg': 'success'})
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


@app.route('/redact_course/<_id>', methods=['GET', 'POST'])  # todo: установка значения дня недели по умолчанию
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
