from flask import Flask, render_template
from db import db_session
from db.models import Course, User

app = Flask(__name__)
db_session.global_init()


@app.route('/', methods=['GET', 'POST'])
def main_page():
    return render_template('index.html')


@app.route('/enroll')   # страница записи ребёнка
def enroll():
    return render_template('enroll.html', title='Запись')


@app.route('/admin')
def admin_panel():
    db_sess = db_session.create_session()
    courses = db_sess.query(Course).all()
    return render_template('admin.html', title='Панель администратора', courses=courses)


if __name__ == '__main__':
    db_session.global_init()
    app.run()
