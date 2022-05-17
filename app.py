from flask import Flask, render_template, request, redirect
from db import db_session
from db.models import Course
from forms import NewCourse, RegisterForm, RegisterChild
import urllib.parse
from pprint import pprint

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super_secret_key'
db_session.global_init()


@app.route('/', methods=['GET', 'POST'])
def main_page():
    return render_template('index.html')


@app.route('/enroll', methods=['GET', 'POST'])  # страница записи ребёнка
def enroll():
    db_sess = db_session.create_session()
    sort_type = request.args.get('sort_type')
    courses = db_sess.query(Course).all()
    nav_areas = list(set([course.area for course in courses]))
    if not sort_type:
        pass
    elif sort_type.split('_')[0] != 'age':
        sort_type, sort_data = sort_type.split('_')
        courses = eval(f'list(filter(lambda x: x.{sort_type} == "{sort_data}", courses))')
    else:
        age = int(sort_type.split('_')[1])
        courses = list(filter(lambda x: x.age_from <= age < x.age_to, courses))
    areas = {}
    directions = set()
    form = RegisterChild()
    for course in courses:
        if course.area in areas:
            if course.direction not in areas[course.area]:
                areas[course.area].append(course.direction)
                directions.add(course.direction)
            else:
                continue
        else:
            areas[course.area] = [course.direction]
            directions.add(course.direction)
    directions = list(directions)
    if request.method == 'POST':
        data = request.form.to_dict()
        pprint(data)
    return render_template('enroll.html', title='Запись', courses=courses, areas=areas, directions=directions,
                           form=form, nav_areas=nav_areas)


@app.route('/registration', methods=['POST'])
def registration():
    if request.method == 'POST':
        data = request.form.to_dict()
        pprint(data)


@app.route('/admin')  # панель администратора
def admin_panel():
    db_sess = db_session.create_session()
    courses = db_sess.query(Course).all()
    return render_template('admin.html', title='Панель администратора', courses=courses)


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
    return render_template('add_course.html', title='Добавить новое объединение', form=form)


if __name__ == '__main__':
    db_session.global_init()
    app.run()
