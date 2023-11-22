from wtforms import StringField, PasswordField, validators, ValidationError
from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash
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

    def get_user(self) -> User | None:
        return User.query.filter_by(email=self.email.data).first()
    
    def validate_user(self):
        user = self.get_user()
        if not (user and check_password_hash(user.password, self.password.data)):
            raise ValidationError('Неверный логин или пароль.')
