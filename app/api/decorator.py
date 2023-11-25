"""Route function decorator."""
import jwt
from flask import request, current_app
from config import JWT_HSH_FUNC
from app.models import User
from werkzeug.security import check_password_hash
from functools import wraps


def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "Authorization" in request.headers:
            token = request.headers.get("Authorization")
            if token:
                try:
                    data = jwt.decode(token, current_app.secret_key, algorithms=[JWT_HSH_FUNC])
                    user = User.query.filter_by(email=data["email"]).first()
                    if not user:
                        return {"message": "user not found"}, 401
                    if not check_password_hash(user.password, data["password"]):
                        return {"message": "password invalid"}, 401

                except Exception as ex:
                    return {"message": "Invalid token", "error": str(ex)}, 401
            else:
                return {"message": "Authentication token required"}, 401
        else:
            return {"message": "Authorization required"}, 401

        return func(*args, **kwargs)

    return wrapper
