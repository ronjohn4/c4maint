from flask import Blueprint

bp = Blueprint('env', __name__, template_folder='templates')

from app.env import routes
