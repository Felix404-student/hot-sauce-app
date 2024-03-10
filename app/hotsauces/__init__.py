from flask import Blueprint

bp = Blueprint('hotsauces', __name__)


from app.hotsauces import routes
