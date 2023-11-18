"""Routes of main blueprint."""
from loguru import logger
from app.main import bp
from flask import request, redirect, url_for, render_template, current_app, session
from app.extensions import mail
from flask_mail import Message


@bp.route('/')
def index():
    # session.clear() # TODO: нужно только для проверки корзины, потом удалить!!!
    if 'cart' not in session:
        session['cart'] = {'products': {}, 'total': 0}
    return render_template('index.html')

@bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        email = request.form.get('email')
        phone = request.form.get('phone')
        recipient = current_app.config.get('MAIL_USERNAME')
        msg = Message('Обратная связь', recipients=[recipient])
        msg.body = f'Вы получили сообщение от пользователя: email: {email}, телефон: {phone}'
        mail.send(msg)
    return redirect(url_for('main.index'))

@bp.route('/agreement')
def agreement():
    return render_template('documents/agreement.html')

@bp.route('/privacy-policy')
def privacy_policy():
    return render_template('documents/privacy-policy.html')

@bp.route('/requisites')
def requisites():
    return render_template('documents/requisites.html')

@bp.route('/guarantees-and-ereturns')
def guarantees_ereturns():
    return render_template('information/guarantees-and-ereturns.html')

@bp.route('/payment-delivery')
def payment_delivery():
    return render_template('information/payment-delivery.html')

@bp.route('/help')
def help():
    return render_template('information/help.html')
