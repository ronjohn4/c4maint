from flask import Blueprint

bp = Blueprint('keyval', __name__, template_folder='templates')
print(f"name:{__name__}")
from app.keyval import routes
