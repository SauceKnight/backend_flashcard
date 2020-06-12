from flask import Blueprint, request
from ..models import Card, db, Deck


bp = Blueprint("cards", __name__, url_prefix="")


@bp.route("/cards")
def get_cards():
    cards = Card.query.all()
    data = [{
        "id": card.id,
        "deck_id": card.deck_id,
        "question": card.question,
        "answer": card.answer
    } for card in cards]
    return {"data": data}


@bp.route("/cards/<deckid>")
def get_cards_by_deck(deckid):
    cards = Card.query.filter_by(deck_id=deckid).all()
    data = {}
    for card in cards:
        data[card.id] = {"id": card.id,
                         "question": card.question, "answer": card.answer, "deck_id": card.deck_id}
    return {"data": data}


@bp.route("/cards/<int:deckId>/<int:cardId>")
def get_single_card_by_deck(deckId, cardId):
    card = Card.query.filter_by(deck_id=deckId).filter_by(id=cardId).first()
    print(cardId)
    data = {
        "id": card.id,
        "deck_id": card.deck_id,
        "question": card.question,
        "answer": card.answer
    }
    return {"data": data}


@bp.route("/cards/<deckid>", methods=["POST"])
def post_cards_by_deck(deckid):
    deck = Deck.query.filter_by(id=deckid).first()
    if not deck:
        return "Deck doesn't exist", 404
    data = request.json
    data["deck"] = deck
    card = Card(**data)
    db.session.add(card)
    db.session.commit()
    data = {}
    data[card.id] = {"id": card.id,
                     "question": card.question, "answer": card.answer, "deck_id": card.deck_id}
    return {
        "data": data
    }
