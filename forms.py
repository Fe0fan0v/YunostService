from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, SubmitField, PasswordField, DateField, TelField, SelectField, IntegerField
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
