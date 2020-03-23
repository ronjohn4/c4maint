from flask import Blueprint

bp = Blueprint('app', __name__, template_folder='templates')
print(f"name:{__name__}")
from app.app import routes
