from flask import Blueprint, request
from ..models import Card, db, Completed, Deck


bp = Blueprint("completed", __name__, url_prefix="")


@bp.route("/<userid>/<deckid>/completed")
def get_completed_cards(userid, deckid):
    cards = Card.query.filter_by(deck_id=deckid).all()
    print(cards)
    completeCount = 0
    for card in cards:
        try:
            completed = Completed.query.filter_by(
                user_id=userid, card_id=card.id).one()
            if completed:
                completeCount += 1
        except:
            pass
    data = [{
        "completeCount": completeCount,
    }]
    return {"data": data}


@bp.route("/<userid>/<cardid>/complete", methods=["POST"])
def post_cards_to_completed(userid, cardid):
    card = Card.query.filter_by(id=cardid).first()
    if not card:
        return "Card doesn't exist", 404
    data = request.json
    print(request.json)
    completed = Completed(**data)
    db.session.add(completed)
    db.session.commit()
    return {
        "id": completed.id,
        "card_id": completed.card_id,
        "user_id": completed.user_id,
    }
