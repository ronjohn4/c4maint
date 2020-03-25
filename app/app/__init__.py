from flask import Blueprint

bp = Blueprint('app', __name__, template_folder='templates')

from app.app import routes
