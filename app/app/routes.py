from flask import render_template, redirect, url_for, request, current_app
from app import db
from app.app import bp
from app.models import App, ParentAudit
from app.app.forms import AppForm
from datetime import datetime
from app.models import load_user
from flask_login import login_required, current_user


lastpagefull = 0
lastpagefilter = 0
next_page = None


@bp.route('/list/')
@login_required
def applist():
    global lastpagefull

    page = request.args.get('page', lastpagefull, type=int)
    lastpagefull = page
    applist = App.query.paginate(page, current_app.config['ROWS_PER_PAGE_FULL'], False)
    next_url = url_for('.applist', page=applist.next_num) if applist.has_next else None
    prev_url = url_for('.applist', page=applist.prev_num) if applist.has_prev else None
    return render_template('applist.html', apps=applist.items, next_url=next_url, prev_url=prev_url)


@bp.route('/add/', methods=["GET", "POST"])
@login_required
def appadd():
    form = AppForm()
    if request.method == 'POST' and form.validate_on_submit():
        var = App(name=request.form['name'], is_active='is_active' in request.form)
        db.session.add(var)
        db.session.commit()
        return redirect('/app/list')
    return render_template('appadd.html', form=form)


@bp.route('/view/<int:id>', methods=["GET", "POST"])
@login_required
def appview(id):
    global lastpagefilter

    page = request.args.get('page', lastpagefilter, type=int)
    lastpagefilter = page
    appsingle = App.query.filter_by(id=id).first_or_404()
    auditlist = ParentAudit.query.\
        filter_by(parent_id=appsingle.id).paginate(page, current_app.config['ROWS_PER_PAGE_FILTER'], False)
    next_url = url_for('.appview', id=id, page=auditlist.next_num) if auditlist.has_next else None
    prev_url = url_for('.appview', id=id, page=auditlist.prev_num) if auditlist.has_prev else None
    return render_template('appview.html', app=appsingle, auditlist=auditlist.items, next_url=next_url,
                           prev_url=prev_url)


@bp.route('/edit/<int:id>', methods=["GET", "POST"])
@login_required
def appedit(id):
    global next_page

    form = AppForm()
    if request.method == "POST" and form.validate_on_submit():
        data = App.query.filter_by(id=id).first_or_404()
        before = str(data.to_dict())
        data.name = request.form['name']
        data.is_active = 'is_active' in request.form

        after = str(data.to_dict())
        var = ParentAudit(parent_id=data.id,
                          a_datetime=datetime.now(),
                          a_user_id=current_user.id,
                          a_username=load_user(current_user.id).username,
                          action="change",
                          before=before,
                          after=after
                          )

        db.session.add(var)
        db.session.commit()
        return redirect(next_page)

    if request.method == 'GET':
        next_page = request.referrer
        appsingle = App.query.filter_by(id=id).first_or_404()
        form.load(appsingle)
    return render_template('appedit.html', form=form, next=request.referrer)


@bp.route('/delete/<int:id>', methods=["GET", "POST"])
@login_required
def appdelete(id):
    global lastpagefull

    App.query.filter_by(id=id).delete()
    db.session.commit()

    page = request.args.get('page', lastpagefull, type=int)
    lastpagefull = page
    applist = App.query.paginate(page, current_app.config['ROWS_PER_PAGE_FULL'], False)
    next_url = url_for('.applist', page=applist.next_num) if applist.has_next else None
    prev_url = url_for('.applist', page=applist.prev_num) if applist.has_prev else None
    return render_template('applist.html', apps=applist.items, next_url=next_url, prev_url=prev_url)


# Use to add test data to the App model.
# /app/appaddtest?addcount=30 adds 30 entries
# may need to remove the @login_required
@bp.route('/appaddtest/', methods=["GET", "POST"])
@login_required
def appaddtest():
    addcount = request.args.get('addcount', 20, type=int)
    for addone in range(addcount):
        var = App(name=f'name{addone}',
                     is_active=0
                     )
        db.session.add(var)
    db.session.commit()
    return redirect('/list')
