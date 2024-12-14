from flask import Blueprint

wishlist_bp = Blueprint('wishlist', __name__, template_folder='templates', static_folder='static')

from . import routes
