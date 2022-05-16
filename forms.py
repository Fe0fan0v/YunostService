from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, SubmitField, PasswordField, DateField, TelField, SelectField, IntegerField, \
    TextAreaField, TimeField, BooleanField
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
                                     'Конструирование, моделирование', 'Спорт', 'Шахматы', 'Английский язык',
                                     'Подготовка к школе',
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


class RegisterChild(FlaskForm):
    child_name = StringField('Имя ребенка', validators=[DataRequired()])
    child_surname = StringField('Фамилия ребенка', validators=[DataRequired()])
    child_patronymic = StringField('Отчество ребенка', validators=[DataRequired()])
    child_birthday = DateField('Дата рождения ребенка', validators=[DataRequired()])
    educational_institution = StringField('Школа/детский сад', validators=[DataRequired()])
    edu_class = StringField('Класс в школе', validators=[DataRequired()])
    health = SelectField('Здоровье', validators=[DataRequired()], choices=['Здоров', 'ОВЗ', 'Инвалид'])
    child_phone = StringField('Телефон ребенка', validators=[DataRequired()])
    child_email = EmailField('Email ребенка', validators=[DataRequired()])
    child_residence = StringField('Место жительства ребенка', validators=[DataRequired()])
    # -------------информация о родителе------------#
    parent_name = StringField('Имя родителя/законного представителя', validators=[DataRequired()])
    parent_surname = StringField('Фамилия родителя/законного представителя', validators=[DataRequired()])
    parent_patronymic = StringField('Отчество родителя/законного представителя', validators=[DataRequired()])
    parent_birthday = DateField('Дата рождения родителя/законного представителя', validators=[DataRequired()])
    parent_residence = StringField('Место жительства родителя/законного представителя', validators=[DataRequired()])
    parent_work = StringField('Место работы родителя/законного представителя', validators=[DataRequired()])
    parent_phone = StringField('Телефон родителя/законного представителя', validators=[DataRequired()])
    parent_email = EmailField('Email родителя/законного представителя', validators=[DataRequired()])
    full_family = SelectField('Полная семья', validators=[DataRequired()], choices=['Полная семья', 'Неполная семья'])
    large_family = SelectField('Многодетная семья', validators=[DataRequired()], choices=['Многодетная семья', 'Нет'])
    without_parents = SelectField('Оставшийся без попечения родителей', validators=[DataRequired()],
                                  choices=['Оставшийся без попечения родителей', 'Нет'])
    police_record = SelectField('Состоит на учете в инспекции по делах н/летних', validators=[DataRequired()],
                                choices=['Состоит на учете в инспекции по делах н/летних', 'Нет'])
    resident = SelectField('Гражданин РФ', validators=[DataRequired()],
                           choices=['Гражданин РФ', 'Не является гражданином РФ'])
    second_parent_fio = StringField('ФИО второго родителя')
    second_parent_phone = StringField('Телефон второго родителя')
    submit = SubmitField('Записаться')
