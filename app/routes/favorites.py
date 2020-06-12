from flask import Blueprint, request
from ..models import db, Deck, User, Favorite

bp = Blueprint("favorites", __name__, url_prefix="")


@bp.route("/<int:userid>/decks/favorites")
# get favorites by user id
def get_favorites(userid):
    favorites = Favorite.query.options(db.joinedload(
        "favdeck")).filter_by(user_id=userid).all()

    data = [
        favorite.deck_id
        for favorite in favorites]
    return {"data": data}


@bp.route("/<int:userid>/<int:deckid>/favorites", methods=['POST'])
# push favorite deck into favorites
def post_favorites(userid, deckid):
    data = request.json
    deck = Deck.query.filter_by(id=deckid).first()
    favorites = Favorite(**data)
    db.session.add(favorites)
    db.session.commit()
    decks = {}
    fav = {}
    fav[favorites.id] = {"deck_id": deck.id}
    decks[deck.id] = {"id": deck.id, "title": deck.title}
    return {
        "decks": decks,
        "fav": favorites.deck_id
    }


@bp.route("/<int:userid>/<int:deckid>/favoritedelete", methods=['DELETE'])
# push favorite deck into favorites
def delete_favorites(userid, deckid):
    data = request.json
    favorite = Favorite.query.filter_by(user_id=userid, deck_id=deckid).first()
    db.session.delete(favorite)
    db.session.commit()
    user = User.query.options(db.joinedload("favoriteDecks")).filter_by(
        id=userid).first()
    fav_deck_ids = []
    decks = {}
    for deck in user.favoriteDecks:
        fav_deck_ids.append(deck.id)
        decks[deck.id] = {"id": deck.id, "title": deck.title}
    return {"decks": decks, "favoritedecks": fav_deck_ids}
