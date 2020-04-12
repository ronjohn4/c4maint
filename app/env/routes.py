from flask import render_template, redirect, url_for, request, current_app
from flask_login import login_required, current_user
from app import db
from app.env import bp
from app.models import Env, ParentAudit, load_user
from app.env.forms import EnvForm
from datetime import datetime


lastpagefull = 0
lastpagefilter = 0
next_page = None


@bp.route('/list/')
@login_required
def envlist():
    global lastpagefull

    page = request.args.get('page', lastpagefull, type=int)
    lastpagefull = page
    envlist = Env.query.paginate(page, current_app.config['ROWS_PER_PAGE_FULL'], False)
    next_url = url_for('.envlist', page=envlist.next_num) if envlist.has_next else None
    prev_url = url_for('.envlist', page=envlist.prev_num) if envlist.has_prev else None
    return render_template('envlist.html', envs=envlist.items, next_url=next_url, prev_url=prev_url)


@bp.route('/add/', methods=["GET", "POST"])
@login_required
def envadd():
    form = EnvForm()
    if request.method == 'POST' and form.validate_on_submit():
        var = Env(name=request.form['name'], is_active='is_active' in request.form)
        db.session.add(var)
        db.session.commit()
        return redirect('/env/list')
    return render_template('envadd.html', form=form)


@bp.route('/view/<int:id>', methods=["GET", "POST"])
@login_required
def envview(id):
    global lastpagefilter

    page = request.args.get('page', lastpagefilter, type=int)
    lastpagefilter = page
    envsingle = Env.query.filter_by(id=id).first_or_404()
    auditlist = ParentAudit.query.\
        filter_by(parent_id=envsingle.id).paginate(page, current_app.config['ROWS_PER_PAGE_FILTER'], False)
    next_url = url_for('.envview', id=id, page=auditlist.next_num) if auditlist.has_next else None
    prev_url = url_for('.envview', id=id, page=auditlist.prev_num) if auditlist.has_prev else None
    return render_template('envview.html', env=envsingle, auditlist=auditlist.items, next_url=next_url,
                           prev_url=prev_url)


@bp.route('/edit/<int:id>', methods=["GET", "POST"])
@login_required
def envedit(id):
    global next_page

    form = EnvForm()
    if request.method == "POST" and form.validate_on_submit():
        data = Env.query.filter_by(id=id).first_or_404()
        before = str(data.to_dict())
        data.name = request.form['name']
        data.desc = request.form['desc']
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
        envsingle = Env.query.filter_by(id=id).first_or_404()
        form.load(envsingle)
    return render_template('envedit.html', form=form, next=request.referrer)


@bp.route('/delete/<int:id>', methods=["GET", "POST"])
@login_required
def envdelete(id):
    global lastpagefull

    Env.query.filter_by(id=id).delete()
    db.session.commit()

    page = request.args.get('page', lastpagefull, type=int)
    lastpagefull = page
    envlist = Env.query.paginate(page, current_app.config['ROWS_PER_PAGE_FULL'], False)
    next_url = url_for('.envlist', page=envlist.next_num) if envlist.has_next else None
    prev_url = url_for('.envlist', page=envlist.prev_num) if envlist.has_prev else None
    return render_template('envlist.html', envs=envlist.items, next_url=next_url, prev_url=prev_url)


# Use to add test data to the App model.
# /env/envaddtest?addcount=30 adds 30 entries
# may need to remove the @login_required
@bp.route('/envaddtest/', methods=["GET", "POST"])
@login_required
def envaddtest():
    addcount = request.args.get('addcount', 20, type=int)
    for addone in range(addcount):
        var = Env(name=f'name{addone}',
                  desc=f'desc{addone}',
                  is_active=0
                  )
        db.session.add(var)
    db.session.commit()
    return redirect('/list')
