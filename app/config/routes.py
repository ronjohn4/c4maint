from flask import render_template, redirect, url_for, request, current_app
from app import db
from app.config import bp
from app.models import Parent, ParentAudit
from app.main.forms import ParentForm
from datetime import datetime
import dateutil.parser
from app.models import sex


lastpagefull = 0
lastpagefilter = 0
next_page = None


@bp.route('/parents/')
def parents():
    global lastpagefull
    page = request.args.get('page', lastpagefull, type=int)
    lastpagefull = page
    data = Parent.query.paginate(page, current_app.config['ROWS_PER_PAGE_FULL'], False)
    next_url = url_for('.parents', page=data.next_num) if data.has_next else None
    prev_url = url_for('.parents', page=data.prev_num) if data.has_prev else None
    return render_template('parentlist.html', parents=data.items, sex=sex, next_url=next_url, prev_url=prev_url)


@bp.route('/parentadd/', methods=["GET", "POST"])
def parentadd():
    form = ParentForm()
    if request.method == 'POST' and form.validate_on_submit():
        var = Parent(name=request.form['name'],
                     email=request.form['email'],
                     sex=int(request.form['sex']),
                     dob=datetime.strptime(str(dateutil.parser.parse(request.form['dob'])).split(" ", 1)[0],
                                           '%Y-%m-%d'),
                     is_active='is_active' in request.form,
                     income_amount=request.form['income_amount']
                     )
        db.session.add(var)
        db.session.commit()
        return redirect('/parents')
    return render_template('parentadd.html', form=form)


@bp.route('/parentview/<int:id>', methods=["GET", "POST"])
def parentview(id):
    global lastpagefilter
    page = request.args.get('page', lastpagefilter, type=int)
    lastpagefilter = page
    parent = Parent.query.filter_by(id=id).first_or_404()
    children = ParentAudit.query.filter_by(parent_id=parent.id).paginate(page, current_app.config['ROWS_PER_PAGE_FILTER'], False)
    next_url = url_for('.parentview', id=id, page=children.next_num) if children.has_next else None
    prev_url = url_for('.parentview', id=id, page=children.prev_num) if children.has_prev else None
    return render_template('parentview.html', parent=parent, children=children.items,
                           sex=sex, next_url=next_url, prev_url=prev_url)


@bp.route('/parentedit/<int:id>', methods=["GET", "POST"])
def parentedit(id):
    global next_page

    form = ParentForm()
    if request.method == "POST" and form.validate_on_submit():
        data = Parent.query.filter_by(id=id).first_or_404()
        before = data.audit_format()
        data.name = request.form['name']
        data.email = request.form['email']
        data.sex = int(request.form['sex'])
        data.dob = datetime.strptime(str(dateutil.parser.parse(request.form['dob'])).split(" ", 1)[0], '%Y-%m-%d')
        data.is_active = 'is_active' in request.form
        data.income_amount = request.form['income_amount']

        after = data.audit_format()
        var = ParentAudit(parent_id=data.id,
                          a_datetime=datetime.now(),
                          a_user="Ron",
                          action="change",
                          before=before,
                          after=after
                          )

        db.session.add(var)
        db.session.commit()
        return redirect(next_page)

    if request.method == 'GET':
        next_page = request.referrer
        data = Parent.query.filter_by(id=id).first_or_404()
        form.load(data)
    return render_template('parentedit.html', form=form, next=request.referrer)


# Use to add test data to the Parent model.
# /parentaddtest?addcount=30 adds 30 entries
@bp.route('/parentaddtest/', methods=["GET", "POST"])
def parentaddtest():
    addcount = request.args.get('addcount', 20, type=int)
    for addone in range(addcount):
        var = Parent(name=f'name{addone}',
                     email='email@domain.com',
                     sex=0,
                     dob=datetime.strptime('1999-01-01', '%Y-%m-%d'),
                     is_active=0,
                     income_amount=123.45
                     )
        db.session.add(var)
    db.session.commit()
    return redirect('/parents')


# Use to add test data to the ParentAudit model.
# /parentauditaddtest?addcount=30&parentid=3 adds 30 entries to parent 3
@bp.route('/parentauditaddtest/', methods=["GET", "POST"])
def parentauditaddtest():
    addcount = request.args.get('addcount', 20, type=int)
    parentid = request.args.get('parentid', 1, type=int)
    for addone in range(addcount):
        var = ParentAudit(parent_id=parentid,
                          a_datetime=datetime.now(),
                          a_user="Ron",
                          action="change",
                          before="snapshot of parent before",
                          after="snapshot of parent after"
                    )
        db.session.add(var)
    db.session.commit()
    return redirect('/parents')
