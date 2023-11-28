"""Routes of authentication blueprint."""
from loguru import logger
from flask import request, render_template, flash, redirect, url_for, session
from flask_login import login_user, logout_user, current_user, login_required
from app.auth import bp
from app.extensions import db, login_manager
from app.auth.forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash
from app.models import User, Role
import uuid


@login_manager.user_loader
def load_user(id):
    return User.query.get(uuid.UUID(id))

@bp.route('/register', methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form =  RegisterForm()
    if form.validate_on_submit():
        password = generate_password_hash(form.password.data)

        try:
            customer_role = Role.query.filter_by(title='customer').one()
        except Exception as error:
            logger.error(f'Error in retreiving customer role: {error}')
            flash('Произошла ошибка при сохранении данных.', 'danger')
            return render_template('auth/register.html', form=form)

        user = User(
            name=form.name.data,
            email=form.email.data,
            password=password,
            role_id=customer_role.id,
        )

        try:
            db.session.add(user)
            db.session.commit()
        except Exception as error:
            logger.error(f'Db error while adding user: {error}')
            flash('Произошла ошибка при сохранении данных.', 'danger')
            return render_template('auth/register.html', form=form)

        flash('Вы успешно зарегистрировались!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        try:
            form.validate_user()
        except Exception as ex:
            flash(str(ex), 'danger')
            return redirect(url_for('auth.login'))

        user = form.get_user()
        login_user(user)
        next = request.args.get('next')
        return redirect(next or url_for('main.index'))
    return render_template('auth/login.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    session.pop('_flashes', None)
    logout_user()
    return redirect(url_for('main.index'))
