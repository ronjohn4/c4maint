from flask import Blueprint

bp = Blueprint('config', __name__, template_folder='templates')

from app.config import routes
