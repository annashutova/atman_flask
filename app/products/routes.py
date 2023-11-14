"""Routes of products blueprint."""
from loguru import logger
from flask import request, render_template, url_for, session, jsonify
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
        quantity = int(request.form.get('quantity'))
        if 'cart' in session:
            products_data = session['cart']['products'].get(str(product_id))
            if products_data:
                products_data['quantity'] = quantity
            else:
                session['cart']['products'][str(product_id)] = {'product_id': product_id, 'quantity': quantity}
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
                'quantity': session['cart']['products'][product_id]['quantity'],
                'price': product.price * session['cart']['products'][product_id]['quantity']
            }
            session['cart']['total'] += session['cart']['products'][product_id]['price']
            session.modified = True
        return render_template('products/cart.html', cart=session['cart'])
