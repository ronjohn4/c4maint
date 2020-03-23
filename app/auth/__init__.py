from flask import Blueprint

bp = Blueprint('auth', __name__, template_folder='templates')
print(f"name:{__name__}")
from app.auth import routes
