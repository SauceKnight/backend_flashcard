from flask import Blueprint, request
from ..models import db, Deck, User, Favorite

bp = Blueprint("decks", __name__, url_prefix="/user/<int:userid>")


@bp.route("/deck/<int:deckid>")
# get one deck by deck id
def get_deck(userid, deckid):
    deck = Deck.query.filter_by(id=deckid).first()
    data = {}
    data[deckid] = {
        "id": deck.id,
        "title": deck.title}
    return {"data": data}


@bp.route("/decks")
# get all decks for a specific user
def get_all_decks(userid):
    user = User.query.options(db.joinedload("favoriteDecks")).filter_by(
        id=userid).first()
    fav_deck_ids = []
    decks = {}
    for deck in user.favoriteDecks:
        fav_deck_ids.append(deck.id)
        decks[deck.id] = {"id": deck.id, "title": deck.title}
    return {"decks": decks, "favoritedecks": fav_deck_ids}


@bp.route("/new_deck", methods=["POST"])
# make a new deck
def new_deck(userid):
    user = User.query.filter_by(id=userid).first()
    if not user:
        return "User doesn't exist", 404
    data = request.json
    print(type(userid))
    data["user_id"] = userid
    new_deck = Deck(**data)
    favorite = Favorite()
    db.session.add(new_deck)
    db.session.commit()
    favorite.user_id = userid
    favorite.deck_id = new_deck.id
    db.session.add(favorite)
    db.session.commit()
    data = {}
    data[new_deck.id] = {"id": new_deck.id, "title": new_deck.title}
    fav = {}
    fav[favorite.id] = {"deck_id": favorite.deck_id}
    return {
        "data": data,
        "fav": favorite.deck_id
    }
