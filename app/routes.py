from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app import db
from app.models import Parent
from app.forms import ParentForm
from datetime import datetime
import dateutil.parser
from app.models import sex

lastpage = 0


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html', title='Home')


@app.route('/parents')
def parents():
    global lastpage
    page = request.args.get('page', lastpage, type=int)
    lastpage = page
    data = Parent.query.paginate(page, app.config['ROWS_PER_PAGE'], False)
    next_url = url_for('parents', page=data.next_num) if data.has_next else None
    prev_url = url_for('parents', page=data.prev_num) if data.has_prev else None
    return render_template('parentlist.html', parents=data.items, sex=sex,
                           next_url=next_url, prev_url=prev_url)


# todo - show child list for selected parent
@app.route('/parentview/<int:id>', methods=["GET", "POST"])
def parentview(id):
    data = Parent.query.filter_by(id=id).first_or_404()
    return render_template('parentview.html', parent=data, sex=sex)


@app.route('/parentadd2', methods=["GET", "POST"])
def parentadd():
    form = ParentForm()
    if request.method == 'POST' and form.validate_on_submit():
        var = Parent(name=request.form['name'],
                     email=request.form['email'],
                     sex=int(request.form['sex']),
                     dob=datetime.strptime(str(dateutil.parser.parse(request.form['dob'])).split(" ", 1)[0], '%Y-%m-%d'),
                     is_tobacco_user='is_tobacco_user' in request.form,
                     income_amount=request.form['income_amount']
                     )
        db.session.add(var)
        db.session.commit()
        return redirect('/parents')

    if request.method == 'GET':
        pass
    return render_template('parentadd.html', form=form)


@app.route('/parentedit/<int:id>', methods=["GET", "POST"])
def parentedit(id):
    form = ParentForm()
    if request.method == "POST" and form.validate_on_submit():
        data = Parent.query.filter_by(id=id).first_or_404()
        data.name = request.form['name']
        data.email = request.form['email']
        data.sex = int(request.form['sex'])
        data.dob = datetime.strptime(str(dateutil.parser.parse(request.form['dob'])).split(" ", 1)[0], '%Y-%m-%d')
        data.is_tobacco_user = 'is_tobacco_user' in request.form
        data.income_amount = request.form['income_amount']
        db.session.commit()
        return redirect('/parents')

    if request.method == 'GET':
        data = Parent.query.filter_by(id=id).first_or_404()
        form.load(data)
    return render_template('parentedit.html', form=form)


# Use to add test data to parent table.  ?addcount=30 adds 30 entries
@app.route('/parentaddtest', methods=["GET", "POST"])
def parentaddtest():
    addcount = request.args.get('addcount', 20, type=int)
    for addone in range(addcount):
        var = Parent(name=f'name{addone}',
                     email='email@domain.com',
                     sex=0,
                     dob=datetime.strptime('1999-01-01', '%Y-%m-%d'),
                     is_tobacco_user=0,
                     income_amount=123.45
                     )
        db.session.add(var)
        db.session.commit()
    return redirect('/parents')
