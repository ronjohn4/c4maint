from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.models import Parent
from app.forms import ParentForm
from datetime import datetime
import dateutil.parser


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html', title='Home')


@app.route('/parents')
def parents():
    data = Parent.query.all()
    return render_template('parentlist.html', parents=data)


@app.route('/parentview/<int:id>', methods=["GET", "POST"])
def parentview(id):
    data = Parent.query.filter_by(id=id).first_or_404()
    return render_template('parentview.html', parent=data)


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


@app.route('/parentadd', methods=["GET", "POST"])
def parentadd():
    print('parentadd')
    form = ParentForm()
    print(request.method)
    print(form.validate_on_submit())
    if request.method == 'POST' and form.validate_on_submit():
        print('ParentAdd Validated')
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
        print('ParentAdd GET')
        form.validate()
    return render_template('parentadd.html', form=form)
