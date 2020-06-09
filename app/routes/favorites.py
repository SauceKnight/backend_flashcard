from flask import Blueprint, request
from ..models import db, Deck, User, Favorite

bp = Blueprint("favorites", __name__, url_prefix="")


@bp.route("/<int:userid>/decks/favorites")
# get favorites by user id
def get_favorites(userid):
    favorites = Favorite.query.options(db.joinedload(
        "favdeck")).filter_by(user_id=userid).all()

    data = [{
        "deck_id": favorite.deck_id,
        "title": favorite.favdeck.title
    } for favorite in favorites]
    return {"data": data}


@bp.route("/<int:userid>/decks/favorites", methods=['POST'])
# push favorite deck into favorites
def post_favorites(userid):
    data = request.json
    favorites = Favorite(**data)
    db.session.add(favorites)
    db.session.commit()
    return {
        "id": favorites.id,
        "user_id": favorites.user_id,
        "deck_id": favorites.deck_id
    }
