from wtforms import StringField, validators
from flask_wtf import FlaskForm


class UserDataForm(FlaskForm):
    name = StringField('ФИО: ', [validators.DataRequired(message='Это обязательное поле.')])
    email = StringField(
        'Почта: ',
        [validators.Email(message='Невалидная почта.'), validators.DataRequired(message='Это обязательное поле.')]
    )
    phone = StringField(
        'Телефон: ',
        [validators.Regexp(
            r'^\+[0-9]{11}$',
            message=('Телефон записан в неправильном формате. Пример: +79113249567')
        )]
    )
