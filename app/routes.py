from flask import render_template, flash, redirect, url_for, request
from app import app, db
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from app.forms import LoginForm, RegistrationForm
from werkzeug.urls import url_parse
from app.models import Entry

@app.route('/')
@app.route('/index')
@login_required
def index():
    entries = Entry.query.all()
    return render_template('content.html', entries=entries)

#ADD
@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        form = request.form
        bahnhof = form.get('bahnhof')
        beschreibung = form.get('beschreibung')
        if not bahnhof or beschreibung:
            entry = Entry(bahnhof = bahnhof, beschreibung = beschreibung)
            db.session.add(entry)
            db.session.commit()
            return redirect('/')
    return "ERROR"

#UPDATE
@app.route('/update/<int:id>')
def updateRoute(id):
    if not id or id != 0:
        entry = Entry.query.get(id)
        if entry:
            return render_template('update.html', entry=entry)
    return "ERROR"

#UPDATE
@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    if not id or id != 0:
        entry = Entry.query.get(id)
        if entry:
            form = request.form
            bahnhof = form.get('bahnhof')
            beschreibung = form.get('beschreibung')
            entry.bahnhof = bahnhof
            entry.beschreibung = beschreibung
            db.session.commit()
        return redirect('/')
    return "ERROR"

#DELETE
@app.route('/delete/<int:id>')
def delete(id):
    if not id or id != 0:
        entry = Entry.query.get(id)
        if entry:
            db.session.delete(entry)
            db.session.commit()
        return redirect('/')
    return "ERROR"

#LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)



#LOGOUT
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

#REGISTER
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
