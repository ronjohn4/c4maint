from flask import Blueprint

bp = Blueprint('audit', __name__, template_folder='templates')
print(f"name:{__name__}")
from app.audit import routes
