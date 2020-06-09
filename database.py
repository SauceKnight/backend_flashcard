from app.models import User, Deck, Card
from app import app, db
from dotenv import load_dotenv
load_dotenv()

with app.app_context():
    db.drop_all()
    db.create_all()

    user = User(email="test@gmail.com", username="test", password="password")
    deck = Deck(title="Python", user_id=1, description="")
    deck2 = Deck(title="Algorithms", user_id=1, description="")
    cards = [
        Card(deck_id=1, question="1 + 1", answer="2"),
        Card(deck_id=1, question="2 + 2", answer=" 4"),
        Card(deck_id=1, question="3 + 3", answer="6"),
        Card(deck_id=1, question="4 + 4", answer="8"),
    ]

    for card in cards:
        db.session.add(card)

    db.session.add(user)
    db.session.add(deck)
    db.session.add(deck2)

    db.session.commit()
