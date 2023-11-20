from wtforms import StringField, PasswordField, validators, ValidationError
from flask_wtf import FlaskForm
from app.models import User


class RegisterForm(FlaskForm):
    name = StringField('ФИО: ', [validators.DataRequired(message='Это обязательное поле.')])
    email = StringField(
        'Почта: ',
        [validators.Email(message='Невалидная почта.'), validators.DataRequired(message='Это обязательное поле.')]
    )
    password = PasswordField(
        'Пароль: ',
        [
            validators.DataRequired(message='Это обязательное поле.'),
            validators.EqualTo('confirm', message='Пароли должны совпадать!')
        ]
    )
    confirm = PasswordField('Повторите пароль: ', [validators.DataRequired(message='Это обязательное поле.')])

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError('Аккаунт с такой почтой уже существует.')


class LoginForm(FlaskForm):
    email = StringField(
        'Почта: ',
        [validators.Email(message='Невалидная почта.'), validators.DataRequired(message='Это обязательное поле.')]
    )
    password = PasswordField('Пароль: ', [validators.DataRequired(message='Это обязательное поле.')])
