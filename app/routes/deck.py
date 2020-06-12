from flask import Blueprint, request
from ..models import db, Deck, User, Favorite

bp = Blueprint("decks", __name__, url_prefix="/user/<int:userid>")
searchbp = Blueprint("search", __name__, url_prefix="/search")


@bp.route("/deck/<int:deckid>")
# get one deck by deck id
def get_deck(userid, deckid):
    deck = Deck.query.filter_by(id=deckid).first()
    return {
        "id": deck.id,
        "user_id": deck.user_id,
        "title": deck.title,
        "description": deck.description
    }


@bp.route("/decks")
# get all decks for a specific user
def get_all_decks(userid):
    decks = Deck.query.filter_by(user_id=userid).all()
    data = [{
        "id": deck.id,
        "user_id": deck.user_id,
        "title": deck.title,
        "description": deck.description,
    } for deck in decks]
    return {"data": data}


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


@searchbp.route("/decks", methods=["POST"])
# search the deck by title
def search_all_decks():
    data = request.json
    searchTerm = data["searchTerm"]
    decks = Deck.query.filter(Deck.title.ilike(f"%{searchTerm}%"))
    foundDecks = [{
        "id": deck.id,
        "user_id": deck.user_id,
        "title": deck.title,
        "description": deck.description
    } for deck in decks]
    return {"data": foundDecks}
