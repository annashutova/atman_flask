"""Forms for cart blueprint."""
from wtforms import StringField, TextAreaField, TelField, validators
from flask_wtf import FlaskForm


class OrderForm(FlaskForm):
    name = StringField(
        'ФИО: ',
        [validators.DataRequired(message='Это обязательное поле.')],
        description='Как к вам обращаться (можно изменить в профиле)',
        render_kw={'readonly': True}
    )
    phone = TelField(
        'Телефон: ',
        [
            validators.DataRequired(message='Это обязательное поле.'),
            validators.Regexp(r'^\+[0-9]{11}$', message=('Телефон записан в неправильном формате. Пример: +79113249567'))
        ],
        description='Укажите номер телефона, по которому с вами можно связаться'
    )
    address = StringField('Адрес: ', description='Укажите адрес доставки')
    email = StringField(
        'Email: ',
        [validators.Email(message='Невалидная почта.'), validators.DataRequired(message='Это обязательное поле.')],
        description='Почта, по которой с вами можно связаться (можно изменить в профиле)',
        render_kw={'readonly': True}
    )
    extra = TextAreaField('Примечание: ', description='Укажите дополнительную информацию к заказу')
