from flask import Blueprint, request, jsonify, redirect
from ..models import db, User, Deck
from werkzeug.security import generate_password_hash
from app.util import token_required
from app import app
import jwt

bp = Blueprint('users', __name__, url_prefix='')

# register


@bp.route('/signup', methods=['POST'])
def register_user():
    data = request.json
    hashed_password = generate_password_hash(data["password"])
    new_user = User(
        username=data["username"],
        email=data["email"],
        password=hashed_password
    )
    db.session.add(new_user)
    db.session.commit()
    token = jwt.encode({'user_id': new_user.id}, app.config['SECRET_KEY'])
    return {'token': token.decode('UTF-8')}

# # Login


@bp.route('/login', methods=['POST'])
def login_user():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user.check_password(data['password']):
        token = jwt.encode({'user_id': user.id}, app.config['SECRET_KEY'])
        return {'token': token.decode('UTF-8')}
    else:
        return {'message': 'Invalid credentials'}, 401

# get user's profile


@bp.route("/users/<int:userid>")
@token_required
def profile_user(userid, current_user):
    print(userid)
    user = User.query.filter_by(id=userid).first()
    data = [{
        "id": user.id,
        "username": user.username,
        "email": user.email,
    }]
    return {"data": data}

