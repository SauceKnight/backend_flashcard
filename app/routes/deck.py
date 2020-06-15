from flask import Blueprint, request
from ..models import db, Deck, User, Favorite, Card

bp = Blueprint("decks", __name__, url_prefix="/user/<int:userid>")
searchbp = Blueprint("search", __name__, url_prefix="/search")


@bp.route("/deck/<int:deckid>")
# get one deck by deck id
def get_deck(userid, deckid):
    deck = Deck.query.filter_by(id=deckid).first()
    data = {}
    data[deckid] = {
        "id": deck.id,
        "title": deck.title,
        "user_id": deck.user_id, "description": deck.description}
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
        decks[deck.id] = {"id": deck.id,
                          "title": deck.title, "user_id": deck.user_id, "description": deck.description}
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
    data[new_deck.id] = {"id": new_deck.id,
                         "title": new_deck.title, "user_id": new_deck.user_id, "description": new_deck.description}
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


@bp.route("/<deckid>/delete", methods=['DELETE'])
# push favorite deck into favorites
def delete_deck(userid, deckid):
    data = request.json
    deleteDeck = Deck.query.filter_by(user_id=userid, id=deckid).first()
    deleteFavorites = Favorite.query.filter_by(deck_id=deckid).all()
    deleteCards = Card.query.filter_by(deck_id=deckid).all()
    db.session.delete(deleteDeck)
    for favorite in deleteFavorites:
        db.session.delete(favorite)
    for card in deleteCards:
        db.session.delete(card)
    db.session.commit()
    user = User.query.options(db.joinedload("favoriteDecks")).filter_by(
        id=userid).first()
    fav_deck_ids = []
    decks = {}
    for deck in user.favoriteDecks:
        fav_deck_ids.append(deck.id)
        decks[deck.id] = {"id": deck.id,
                          "title": deck.title, "user_id": deck.user_id, "description": deck.description}
    return {"decks": decks, "favoritedecks": fav_deck_ids}


@bp.route("/deck/<deckid>", methods=["PUT"])
def updateDeck(userid, deckid):
    deck = Deck.query.filter_by(id=deckid).first()
    data = request.json
    deck.title = data["title"]
    deck.description = data["description"]
    db.session.commit()
    data = {}
    data[deck.id] = {"id": deck.id,
                     "title": deck.title, "user_id": deck.user_id, "description": deck.description}
    return {
        "data": data
    }
