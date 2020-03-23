from flask import Blueprint

bp = Blueprint('main', __name__, template_folder='templates')
print(f"name:{__name__}")
from app.main import routes
