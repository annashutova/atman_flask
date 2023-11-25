"""Routes of products blueprint."""
from loguru import logger
from flask import render_template, url_for, redirect
from flask_login import login_required, current_user
from app.products import bp
from app.models import Category, Product, OrderDetail
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
    products = Product.query.filter(Product.category_id.is_(None), Product.stock != 0).all()
    return render_template('products/category.html', categories=categories, products=products, breadcrumbs=breadcrumbs)

@bp.route("/category/<uuid:category_id>")
def load_categories(category_id):
    breadcrumbs = get_breadcrumbs(category_id)
    categories = Category.query.filter_by(master_category = category_id).all()
    products = Product.query.filter(Product.category_id == category_id, Product.stock != 0).all()
    return render_template('products/category.html', categories=categories, products=products, breadcrumbs=breadcrumbs)

@bp.route("/product/<uuid:product_id>")
def get_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return redirect(url_for('product.load_catalog'))
    breadcrumbs = get_breadcrumbs(product.category_id)
    return render_template('products/product.html', breadcrumbs=breadcrumbs, product=product)

@bp.route("/orders")
@login_required
def get_user_orders():
    actual_orders = OrderDetail.query.filter(OrderDetail.user_id == current_user.id, OrderDetail.status == 'в процессе').all()
    past_orders = OrderDetail.query.filter(OrderDetail.user_id == current_user.id, OrderDetail.status == 'получен').all()
    return render_template('orders/user_orders.html', actual_orders=actual_orders, past_orders=past_orders)

@bp.route("order/<uuid:order_id>")
@login_required
def get_order(order_id):
    order = OrderDetail.query.get(order_id)
    return render_template('orders/order_item.html', items=order.product_association, order=order)
