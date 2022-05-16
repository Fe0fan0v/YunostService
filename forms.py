from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, SubmitField, PasswordField, DateField, TelField, SelectField, IntegerField, \
    TextAreaField, TimeField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    patronymic = StringField('Отчество', validators=[DataRequired()])
    birthday = DateField('Дата рождения', validators=[DataRequired()])
    address = StringField('Домашний адрес', validators=[DataRequired()])
    phone = TelField('Телефон', validators=[DataRequired()])
    health_class = SelectField('Класс здоровья', validators=[DataRequired()])
    school = IntegerField('Номер школы', validators=[DataRequired()])
    s_class = SelectField('Класс', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')


class NewCourse(FlaskForm):
    name = StringField('Название курса', validators=[DataRequired()])
    direction = SelectField('Направление курса', validators=[DataRequired()],
                            choices=['Изобразительное искусство', 'Вокал', 'Хореография', 'Театр', 'Цирк',
                                     'Развивающая акробатика', 'Журналистика', 'Психология',
                                     'Декоративно-прикладное творчество (валяние из шерсти, бисероплетение, текстильная кукла и др.)',
                                     'Конструирование, моделирование', 'Спорт', 'Шахматы', 'Английский язык', 'Подготовка к школе',
                                     'Естественные науки (химия, биология, астрономия, геология)',
                                     'IT (программирование, робототехника, технический английский и др.)',
                                     'Фотография и видеография'])
    area = SelectField('Площадка проведения курса', validators=[DataRequired()],
                       choices=['Пр-т Макеева, 39', 'Пр-т Октября, 21', 'Ул. Ст. Разина, 4', 'Ул. 8-е марта, 147',
                                'ул. Первомайская, 9'])
    teacher = StringField('Фамилия Имя Отчество педагога', validators=[DataRequired()])
    age_from = StringField('Начало диапазона возраста', validators=[DataRequired()])
    age_to = StringField('Конец диапазона возраста', validators=[DataRequired()])
    group = StringField('Номер группы', validators=[DataRequired()])
    schedule_weekday = SelectField('День недели', validators=[DataRequired()])
    schedule_time = TimeField('Время занятия', validators=[DataRequired()])
    description = TextAreaField('Описание курса', validators=[DataRequired()])
    submit = SubmitField('Сохранить', validators=[DataRequired()])
