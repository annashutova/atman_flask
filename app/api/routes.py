"""API blueprint routes."""
from flask import jsonify, current_app, request, abort
from config import JWT_HSH_FUNC
from app.models import Category, User
from app.api import bp
from app.api.decorator import token_required
from datetime import datetime, timedelta, timezone
from werkzeug.security import check_password_hash
import jwt


@bp.route('/auth', methods=["GET", "POST"])
def auth():
    if request.method == "POST":
        email = request.json.get("email")
        password = request.json.get("password")
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({"message": 'User with these credentials not found'}), 404
        if not check_password_hash(user.password, password):
            return jsonify({"message": 'Invalid password'}), 400
        exp = datetime.now(tz=timezone.utc) + timedelta(hours=1)
        token = jwt.encode(dict(email=email, password=password, exp=exp), current_app.secret_key, algorithm=JWT_HSH_FUNC)
        return jsonify({"message": "token generated successfully", "token": token}), 200
    return abort(405)

@bp.route('/products_categories')
@token_required
def get_products_categories():
    categories = Category.query.all()
    result = {}
    for category in categories:
        result[str(category.id)] = {
            "master_category": category.master_category,
            "title": category.title,
            "image": category.image,
            "products": [
                {
                    "id": product.id,
                    "title": product.title,
                    "desc": product.desc,
                    "price": product.price,
                    "stock": product.stock
                } for product in category.products
            ]
        }
    return jsonify({"categories": result}), 200
