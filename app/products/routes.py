"""Routes of products blueprint."""
from loguru import logger
from flask import request, render_template, flash, redirect, url_for, session
from flask_login import current_user
from app.products import bp
from app.extensions import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import Category, Product
from uuid import UUID


def get_breadcrumbs(category_id: UUID) -> list:
    breadcrumbs = []
    while category_id:
        category = Category.query.get(category_id)
        breadcrumbs.insert(0, {'title': category.title, 'url': url_for('products.load_categories', category_id=category_id)})
        category_id = category.master_category
    breadcrumbs.insert(0, {'title': 'Каталог', 'url': url_for('products.load_catalog')})
    return breadcrumbs

@bp.route("/category/")
def load_catalog():
    breadcrumbs = []
    categories = Category.query.filter_by(master_category = None).all()
    products = Product.query.filter(Product.category_id.is_(None)).all()
    return render_template('products/category.html', categories=categories, products=products, breadcrumbs=breadcrumbs)

@bp.route("/category/<uuid:category_id>")
def load_categories(category_id):
    breadcrumbs = get_breadcrumbs(category_id)
    categories = Category.query.filter_by(master_category = category_id).all()
    products = Product.query.filter_by(category_id = category_id).all()
    return render_template('products/category.html', categories=categories, products=products, breadcrumbs=breadcrumbs)
