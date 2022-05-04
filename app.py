from flask import Flask, render_template, url_for, session
from flask_login import current_user

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def main_page():
    return render_template('index.html')


@app.route('/enroll')   # страница записи ребёнка
def enroll():
    return render_template('enroll.html')


if __name__ == '__main__':
    app.run()
