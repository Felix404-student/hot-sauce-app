from app.extensions import db
from app.models.user import User


class HotSauce(db.Model):
    """HotSauce."""
    __tablename__ = "hot_sauces"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    base = db.Column(db.String(20), nullable=False)
    pepper = db.Column(db.String(20), nullable=False)
    bottle = db.Column(db.String(20), nullable=False)


class Rating(db.Model):
    """User's rating of a hot sauce."""
    __tablename__ = "ratings"
    hotsauce_id = db.Column(db.Integer, db.ForeignKey('hot_sauces.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    flavor = db.Column(db.Integer, nullable=False)
    heat = db.Column(db.Integer, nullable=False)
