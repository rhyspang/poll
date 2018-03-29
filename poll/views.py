#   annotator_audio 
#   --------------------------------------
#
#   Written and maintained by Rhys Pang <rhyspang@qq.com>
#
#   Copyright 2017 rhys. All Rights Reserved.
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.


from __future__ import print_function

from flask import url_for, redirect, request, flash, render_template
from flask_login import login_required, logout_user, login_user, current_user
from sqlalchemy import desc

from poll import forms, models
from poll import app, db, login_manager


@login_manager.user_loader
def load_user(uid):
    return models.User.query.get(uid)


@app.route('/history')
@login_required
def show_history():
    page_index = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))

    all_marked = models.LabellingFile.query.filter(
        models.LabellingFile.user_id.isnot(None)
    ).order_by(
        models.LabellingFile.time_updated.desc()
    )

    if current_user.level < 2:
        posts_page = all_marked

    else:
        posts_page = all_marked.filter_by(
            user_id=current_user.id
        )

    posts_page = posts_page.paginate(page_index,
                                     per_page=page_size,
                                     error_out=True)
    entries = posts_page.items
    return render_template('list.html',
                           error='',
                           entries=entries,
                           posts_page=posts_page,
                           )


@app.route('/status')
@login_required
def show_status():
    return render_template('show_status.html')


@app.route('/labelling', methods=['POST'])
@login_required
def labelling():
    form = forms.AnnotateForm()
    entry = models.LabellingFile.query.get(form.file_id.data)
    if entry:
        entry.user_id = current_user.id
        entry.label = form.label.data
        db.session.add(entry)
        db.session.commit()
        flash('New entry was successfully posted')
        return redirect(url_for('show_entries'))


@app.route('/', methods=["GET"])
@login_required
def show_entries():
    form = forms.AnnotateForm()
    if request.method == "GET":
        file_id = request.args.get('fileId')
        if file_id:
            entry = models.LabellingFile.query.get(file_id)
            return render_template('show_entries.html', entry=entry, form=form)

        entry = models.LabellingFile.query. \
            filter_by(label=None,
                      user_id=current_user.id).first()
        if not entry:
            entry = models.LabellingFile.query. \
                filter_by(label=None, user_id=None). \
                order_by(desc(models.LabellingFile.time_created)).first()
        if entry:
            entry.user_id = current_user.id
            db.session.add(entry)
            db.session.commit()
            return render_template('show_entries.html', entry=entry, form=form)
        return "no unlabelled entry in database"


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if request.method == "GET":
        return render_template("login.html", form=form)
    if request.method == 'POST' and form.validate_on_submit():
        user = models.User.query.filter_by(username=form.username.data,
                                           password=form.password.data).first()
        if user:
            flash('Logged in successfully.')
            login_user(user)
            return redirect(request.args.get('next')
                            or url_for('show_entries'))
        else:
            error = 'invalid username or password.'
            return render_template('login.html', error=error, form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
