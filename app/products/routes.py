"""Routes of products blueprint."""
from loguru import logger
from flask import request, render_template, url_for, session, jsonify, redirect
from app.products import bp
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

@bp.route("/add_to_cart/<uuid:product_id>", methods=['GET', 'POST'])
def add_to_cart(product_id):
    if request.method == 'POST':
        product = Product.query.get(product_id)
        quantity = int(request.form.get('quantity'))
        if 'cart' in session:
            products_data = session['cart']['products'].get(product_id.hex)
            if products_data:
                products_data['quantity'] = quantity
            else:
                session['cart']['products'][product_id.hex] = {
                    'product_id': product_id,
                    'price': float(product.price),
                    'quantity': quantity,
                    'qty_price': float(product.price * quantity)
                }
            session.modified = True
        response_data = {'status': 'success', 'message': 'Product added to cart successfully'}
        return jsonify(response_data)
    return jsonify({'status': 'error', 'message': 'Invalid request'})

@bp.route("/cart")
def cart():
    if 'cart' in session:
        session['cart']['total'] = 0
        for product_id in session['cart']['products']:
            product = Product.query.get(UUID(product_id))
            session['cart']['products'][product_id] = {
                'product_id': product.id,
                'title': product.title,
                'image': product.product_images[0].image if product.product_images else 'noimage.jpg',
                'price': float(product.price),
                'quantity': session['cart']['products'][product_id]['quantity'],
                'qty_price': float(product.price * session['cart']['products'][product_id]['quantity'])
            }
            session['cart']['total'] += session['cart']['products'][product_id]['qty_price']
            session.modified = True
        return render_template('products/cart.html', cart=session['cart'], total=session['cart']['total'])

@bp.route("/increase_quantity/<uuid:product_id>", methods=['POST'])
def increase_quantity(product_id):
    if request.method == 'POST':
        if 'cart' not in session:
            return redirect(url_for('main.index'))
        product_id = product_id.hex
        if product_id in session['cart']['products']:
            product_data = session['cart']['products'][product_id]
            product_data['quantity'] += 1
            product_data['qty_price'] += product_data['price']
            session['cart']['total'] += product_data['price']
            session.modified = True
    return redirect(url_for('products.cart'))

@bp.route("/decrease_quantity/<uuid:product_id>", methods=['POST'])
def decrease_quantity(product_id):
    if request.method == 'POST':
        if 'cart' not in session:
            return redirect(url_for('main.index'))
        product_id = product_id.hex
        if product_id in session['cart']['products']:
            product_data = session['cart']['products'][product_id]
            if product_data['quantity'] > 1:
                product_data['quantity'] -= 1
                product_data['qty_price'] -= product_data['price']
                session['cart']['total'] -= product_data['price']
                session.modified = True
    return redirect(url_for('products.cart'))

@bp.route("/input_quantity/<uuid:product_id>", methods=['POST'])
def input_quantity(product_id):
    if request.method == 'POST':
        quantity = int(request.form.get('quantity'))
        if 'cart' not in session:
            return redirect(url_for('main.index'))
        product_id = product_id.hex
        if product_id in session['cart']['products']:
            product_data = session['cart']['products'][product_id]
            if quantity > 0:
                session['cart']['total'] -= product_data['qty_price']
                product_data['quantity'] = quantity
                product_data['qty_price'] = product_data['price'] * quantity
                session['cart']['total'] += product_data['qty_price']
                session.modified = True
    return redirect(url_for('products.cart'))
