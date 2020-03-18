from flask import render_template
from app import app


lastpagefull = 0
lastpagefilter = 0
next_page = None


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')
