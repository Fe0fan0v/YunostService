from flask import Flask, render_template, request
from db import db_session
from db.models import Course, User
from forms import NewCourse, RegisterForm
import urllib.parse


app = Flask(__name__)
app.config['SECRET_KEY'] = 'super_secret_key'


@app.route('/', methods=['GET', 'POST'])
def main_page():
    return render_template('index.html')


@app.route('/enroll')   # страница записи ребёнка
def enroll():
    return render_template('enroll.html', title='Запись')


@app.route('/admin')    # панель администратора
def admin_panel():
    db_sess = db_session.create_session()
    courses = db_sess.query(Course).all()
    return render_template('admin.html', title='Панель администратора', courses=courses)


@app.route('/add_course', methods=['GET', 'POST'])   # добавление нового курса
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
