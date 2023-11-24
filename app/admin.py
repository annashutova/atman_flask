"""Initialization of admin panel."""
from loguru import logger
from flask import redirect, url_for, request, flash
from flask_login import current_user, login_user, logout_user
from flask_admin import Admin
from app.auth.forms import LoginForm
from flask_admin.contrib import sqla
from werkzeug.utils import secure_filename
from flask_admin import expose, AdminIndexView
from flask_admin.form.upload import FileUploadField
from flask_admin.model.form import InlineFormAdmin
from app.models import User, Role, Product, Category, ProductImage, OrderDetail, OrderItem
from app.extensions import db
from config import ADMIN_PAGE_PAGINATION
import os.path as os_path
from time import time
from uuid import uuid4


def generate_filename(obj, file_data):
    _, file_extension = os_path.splitext(file_data.filename)

    timestamp = int(time())
    random_str = str(uuid4())[:10]

    return secure_filename(f'{timestamp}_{random_str}{file_extension}')


class MyInlineFormAdmin(InlineFormAdmin):
    form_widget_args = {
        'created_at': {
            'disabled': True
        },
        'modified_at': {
            'disabled': True
        }
    }


class MyModelView(sqla.ModelView):
    page_size = ADMIN_PAGE_PAGINATION

    form_widget_args = {
        'created_at': {
            'disabled': True
        },
        'modified_at': {
            'disabled': True
        }
    }

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role.title == 'admin'


class MyAdminIndexView(AdminIndexView):

    @expose('/')
    def index(self):
        if not (current_user.is_authenticated and current_user.role.title == 'admin'):
            return redirect(url_for('.login_view'))
        return super(MyAdminIndexView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        if current_user.is_authenticated and current_user.role.title == 'admin':
            return redirect(url_for('.index'))

        form = LoginForm()
        if request.method == 'POST':
            if form.validate_on_submit():
                try:
                    form.validate_user()
                except Exception as ex:
                    flash(ex, 'danger')
                    return self.render('admin/login.html',form=form)
                user = form.get_user()
                if user.role.title == 'admin':
                    login_user(user)
                    return redirect(url_for('.index'))

            flash('Неверные логин или пароль для администратора', 'danger')
        return self.render('admin/login.html', form=form)

    @expose('/logout/')
    def logout_view(self):
        logout_user()
        return redirect(url_for('.index'))


class RoleView(MyModelView):
    column_searchable_list = ('title',)
    column_filters = ('created_at',)


class UserView(MyModelView):
    column_searchable_list = ('name', 'email')
    column_filters = ('created_at',)
    form_columns = ('name', 'email', 'phone', 'password', 'created_at', 'modified_at', 'role')


class ProductImageInlineModelForm(MyInlineFormAdmin):
    form_label = 'Картинка'
    form_extra_fields = {
        'image': FileUploadField(
            label='Картинка',
            base_path=os_path.join(os_path.dirname(__file__), 'static', 'products'),
            namegen=generate_filename,
            allowed_extensions=['jpg', 'png', 'jpeg']
        )
    }

    def __init__(self):
        return super(ProductImageInlineModelForm, self).__init__(ProductImage)


class ProductView(MyModelView):
    column_searchable_list = ('title',)
    column_filters = ('created_at', 'stock', 'price')
    inline_models = (ProductImageInlineModelForm(),)
    form_columns = (
        'title',
        'desc',
        'price',
        'stock',
        'category',
    )


class CategoryView(MyModelView):
    column_searchable_list = ('title',)
    column_filters = ('created_at', )
    form_columns = ('title', 'image')

    form_extra_fields = {
        'image': FileUploadField(
            label='Картинка',
            base_path=os_path.join(os_path.dirname(__file__), 'static', 'categories'),
            namegen=generate_filename,
            allowed_extensions=['jpg', 'png']
        )
    }


class OrderItemInlineModelForm(MyInlineFormAdmin):
    form_label = 'Товары'

    def __init__(self):
        return super(OrderItemInlineModelForm, self).__init__(OrderItem)


class OrderDetailView(MyModelView):
    column_searchable_list = ('phone', 'address', 'status')
    column_filters = ('created_at', )
    form_columns = ('user', 'total', 'phone', 'address', 'extra', 'status')
    inline_models = (OrderItemInlineModelForm(), )


admin = Admin(name='Atman', index_view=MyAdminIndexView(), template_mode='bootstrap4')
admin.add_view(RoleView(Role, db.session, 'Роли'))
admin.add_view(UserView(User, db.session, 'Пользователи'))
admin.add_view(CategoryView(Category, db.session, 'Категории'))
admin.add_view(ProductView(Product, db.session, 'Товары'))
admin.add_view(OrderDetailView(OrderDetail, db.session, 'Заказы'))
