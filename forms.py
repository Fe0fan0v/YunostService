from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, SubmitField, PasswordField, DateField, TelField, SelectField, IntegerField, \
    TextAreaField, TimeField, BooleanField, ValidationError, FieldList, FormField, Form
from wtforms.validators import DataRequired, Email
import datetime
from db.db_session import create_db_session
from db.models import Course


class RegisterChild(FlaskForm):
    child_name = StringField('Имя ребенка', validators=[DataRequired()])
    child_surname = StringField('Фамилия ребенка', validators=[DataRequired()])
    child_patronymic = StringField('Отчество ребенка', validators=[DataRequired()])
    child_birthday = DateField('Дата рождения ребенка', validators=[DataRequired()])
    educational_institution = StringField('Школа/детский сад/другое', validators=[DataRequired()])
    edu_class = StringField('Класс/курс (на 1 сентября)', validators=[DataRequired()])
    health = SelectField('Здоровье', validators=[DataRequired()], choices=['Здоров', 'ОВЗ', 'Инвалид'])
    snils = StringField('Номер СНИЛС ребенка')
    certificate = StringField('Номер сертификата вноситься после 31 августа с сайта Госуслуги')
    child_phone = StringField('Телефон ребенка')
    child_email = EmailField('Email ребенка')
    child_residence = StringField('Место жительства ребенка', validators=[DataRequired()])
    # -------------информация о родителе------------#
    parent_name = StringField('Имя родителя/законного представителя', validators=[DataRequired()])
    parent_surname = StringField('Фамилия родителя/законного представителя', validators=[DataRequired()])
    parent_patronymic = StringField('Отчество родителя/законного представителя', validators=[DataRequired()])
    parent_birthday = DateField('Дата рождения родителя/законного представителя', validators=[DataRequired()])
    parent_residence = StringField('Место жительства родителя/законного представителя', validators=[DataRequired()])
    parent_work = StringField('Место работы родителя/законного представителя', validators=[DataRequired()])
    parent_phone = StringField('Телефон родителя/законного представителя', validators=[DataRequired()])
    parent_email = EmailField('Email родителя/законного представителя', validators=[DataRequired(), Email()])
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

    def validate_age(self, course_age):
        age = (datetime.date.today() - self.child_birthday.data).days // 365
        if age >= course_age:
            return True
        else:
            raise ValidationError('Возраст ребёнка слишком мал, пожалуйста выберите более подходящее объединение.')


class AdminEnter(FlaskForm):
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class CourseForm(Form):
    old_name = StringField('Название')
    old_group = StringField('Номер группы')
    new_name = SelectField('Название')
    new_group = SelectField('Номер группы')
