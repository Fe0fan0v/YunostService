from flask import Flask, render_template, request
from db import db_session
from db.models import Course, User
from forms import NewCourse, RegisterForm


app = Flask(__name__)
db_session.global_init()
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
        info = data.to_dict()
        area = info['area']
        direction = info['direction']
        description = info['description']
        groups = data.getlist('group[]')
        weekdays = data.getlist('weekday[]')
        times = data.getlist('time[]')
        print(info)
    return render_template('add_course.html', title='Добавить новое объединение', form=form)


if __name__ == '__main__':
    db_session.global_init()
    app.run()
