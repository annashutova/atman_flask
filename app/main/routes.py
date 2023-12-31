"""Routes of main blueprint."""
from loguru import logger
from app.main import bp
from app.main.forms import UserDataForm
from flask import request, redirect, url_for, render_template, current_app, session, jsonify, flash
from flask_login import current_user, login_required
from app.extensions import mail, db
from flask_mail import Message
from app.models import Product, Category


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

@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

    form = UserDataForm(obj=current_user)
    if form.validate_on_submit():
        form_data = form.data

        current_user.name = form_data.get('name')
        current_user.email = form_data.get('email')
        current_user.phone = form_data.get('phone')

        db.session.commit()
        flash('Данные успешно сохранены!', 'success')

    for error in form.errors:
        if not (form[error].name == 'phone' and form.data.get('phone') is None):
            flash(f'{form[error].label.text}{form.errors[error][0]}', 'danger')
    return render_template('profile.html', form=form)

@bp.route("/search")
def search():
    query = request.args.get('query', '')

    product_results = Product.query.filter(Product.title.ilike(f'%{query}%')).all()
    category_results = Category.query.filter(Category.title.ilike(f'%{query}%')).all()

    results = []
    if category_results:
        results += [{'type': 'header', 'title': 'Категории'}]
    results += [
        {
            'url': url_for('products.load_categories', category_id=category.id),
            'title': category.title,
            'type': 'category'
        } for category in category_results
    ]
    if product_results:
        results += [{'type': 'header', 'title': 'Товары'}]
    results += [
        {
            'url': url_for('products.get_product', product_id=product.id),
            'title': product.title,
            'type': 'product'
        } for product in product_results
    ]
    return jsonify(results)
