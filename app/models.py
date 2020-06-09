from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

    decks = db.relationship("Deck", back_populates="user")
    # card_completed = db.relationship(
    #     "Completed", back_populates="user_details")

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Deck(db.Model):
    __tablename__ = "decks"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(300))

    cards = db.relationship("Card", back_populates="deck")
    user = db.relationship("User", back_populates="decks")


class Card(db.Model):
    __tablename__ = "cards"
    id = db.Column(db.Integer, primary_key=True)
    deck_id = db.Column(db.Integer, db.ForeignKey("decks.id"), nullable=False)
    question = db.Column(db.String(200), nullable=False)
    answer = db.Column(db.String(200), nullable=False)

    deck = db.relationship("Deck", back_populates="cards")
    # user_completed = db.relationship(
    #     "Completed", back_populates="card_details")


class Completed(db.Model):
    __tablename__ = "completed"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    card_id = db.Column(db.Integer, db.ForeignKey("cards.id"), nullable=False)

    # user_details = db.relationship("User", back_populates="card_completed")
    # card_details = db.relationship("Card", back_populates="user_completed")


class Favorite(db.Model):
    __tablename__ = "favorite"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    deck_id = db.Column(db.Integer, db.ForeignKey("decks.id"), nullable=False)
