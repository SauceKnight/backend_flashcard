import jwt
from flask import jsonify, request
from app.routes.user import User
from functools import wraps
from app import app


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return {'message': 'a valid token is missing'}
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            print("data", data)
            current_user = User.query.filter_by(id=data['id']).first()
        except:
            return {'message': 'token is invalid'}, 401
        return f(current_user=current_user, *args, **kwargs)
    return decorator
