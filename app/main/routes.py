"""Routes of main blueprint."""
from loguru import logger
from app.main import bp
from flask import request, redirect, url_for, make_response, render_template, current_app
from app.extensions import mail
from flask_mail import Message


@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        email = request.form.get('email')
        phone = request.form.get('phone')
        site_email = current_app.config.get('MAIL_USERNAME')
        msg = Message('Обратная связь', recipients=[site_email])
        msg.body = f'Вы получили сообщение от пользователя: email: {email}, телефон: {phone}'
        mail.send(msg)
        logger.info('Email successfuly sent')
    return redirect(url_for('main.index'))
