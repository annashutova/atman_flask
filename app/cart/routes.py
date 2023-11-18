"""Routes of cart blueprint."""
from loguru import logger
from flask import request, render_template, url_for, session, jsonify, redirect
from flask_login import login_required
from app.cart import bp
from app.models import Product
from uuid import UUID


@bp.route("/cart")
@login_required
def get_cart():
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
                'qty_price': float(product.price * session['cart']['products'][product_id]['quantity']),
                'stock': product.stock
            }
            session['cart']['total'] += session['cart']['products'][product_id]['qty_price']
            session.modified = True
        return render_template('cart.html', cart=session['cart'], total=session['cart']['total'])
    return redirect(url_for('main.index'))

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

@bp.route("/input_quantity/<uuid:product_id>", methods=['GET', 'POST'])
def input_quantity(product_id):
    if request.method == 'POST':
        if 'cart' not in session:
            return jsonify({'status': 'error', 'message': 'Cart not in session'})
        quantity = int(request.form.get('quantity'))
        product_id = product_id.hex
        if product_id in session['cart']['products']:
            product_data = session['cart']['products'][product_id]
            if quantity > 0:
                session['cart']['total'] -= product_data['qty_price']
                product_data['quantity'] = quantity
                product_data['qty_price'] = product_data['price'] * quantity
                session['cart']['total'] += product_data['qty_price']
                session.modified = True
                response = {
                    'status': 'success',
                    'qty_price': product_data['qty_price'],
                    'total': session['cart']['total']
                }
                return jsonify(response)
    return jsonify({'status': 'error', 'message': 'Invalid request'})

@bp.route("/remove_from_cart/<uuid:product_id>", methods=['GET', 'POST'])
def remove_from_cart(product_id):
    if request.method == 'POST':
        if 'cart' in session:
            product_id = product_id.hex
            if product_id in session['cart']['products']:
                product_data = session['cart']['products'].pop(product_id)
                session['cart']['total'] -= product_data['qty_price']
            session.modified = True
    return redirect(url_for('cart.get_cart'))
