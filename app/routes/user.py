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
    token = jwt.encode(
        {"id": new_user.id, "username": new_user.username, "favoritedecks": [], "decks": {}}, app.config['SECRET_KEY'])
    return {'token': token.decode('UTF-8'), "id": new_user.id, "username": new_user.username}

# # Login


@bp.route('/login', methods=['POST'])
def login_user():
    data = request.json
    print(data["username"])
    user = User.query.options(db.joinedload("favoriteDecks")).filter_by(
        username=data['username']).first()
    if user.check_password(data['password']):
        fav_deck_ids = []
        decks = {}
        for deck in user.favoriteDecks:
            fav_deck_ids.append(deck.id)
            decks[deck.id] = {"id": deck.id,
                              "title": deck.title, "user_id": deck.user_id}
        print(fav_deck_ids)
        print(user.favoriteDecks)
        token = jwt.encode(
            {"id": user.id, "username": user.username, "favoritedecks": fav_deck_ids, "decks": decks}, app.config['SECRET_KEY'])
        return {'token': token.decode('UTF-8'), "id": user.id, "username": user.username, "favoritedecks": fav_deck_ids, "decks": decks}
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
