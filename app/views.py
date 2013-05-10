#imports
from __future__ import with_statement
import sqlite3
import db
from flask import Flask, request, session, g, redirect, url_for, \
	abort, render_template, flash
from forms import *
from flask.ext.login import (LoginManager, current_user, login_required,
                            login_user, logout_user, UserMixin, AnonymousUser,
                            confirm_login, fresh_login_required)
from app import app
from models import *

from flaskext.bcrypt import Bcrypt

bcrypt = Bcrypt(app)

login_manager = LoginManager()

login_manager.anonymous_user = Anonymous
login_manager.login_view = "login"
login_manager.login_message = u"Please log in to access this page."
login_manager.refresh_view = "reauth"

login_manager.setup_app(app)

@app.before_request
def before_request():
    g.db = db.connect_db()

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

@app.route('/')
def explore():
    curUser = (current_user.get_id() or "Not Logged In")
    if (curUser != "Not Logged In" and curUser != None):
        curUser = db.curUsername(curUser)
    cur = g.db.execute('select name from nodes order by id')
    nodes = [dict(name=row[0]) for row in cur.fetchall()]
    return render_template('explore.html', nodes=nodes, curUser= curUser)

@app.route('/build')
def build():
    cur = g.db.execute('select name from nodes order by id')
    nodes = [dict(name=row[0]) for row in cur.fetchall()]
    return render_template('build.html', nodes=nodes)

@app.route('/contact')
def contact():
    return render_template('base.html')

@app.route('/about')
def about():
    return render_template('base.html')

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        about(401)
    g.db.execute('insert into nodes (name, lon, lat) values (?, ?, ?)',
        [request.form['name'], request.form['lon'], request.form['lat']])
    g.db.commit()

    flash('New node added')
    return redirect(url_for('explore'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember_me.data
        user = db.pullUserObj(username, password)
        if user is None: #Correct username and password?
            flash("Incorrect Username or Password")
            return redirect('/login')
        if login_user(user ,remember): #Everything looks good attempt login.
            return redirect('/')
        else:
            flash("Login Failed")    
        return redirect('/login')
    return render_template('login.html', title= 'Sign In', form = form)


@login_manager.user_loader
def load_user(id):
    g.db = db.connect_db() # Since this isn't a request we need to connect first.
    user = db.query_db('select * from users where id = ?', [id], one=True)
    g.db.close()
    return User(user['id'], user['username'], user['password'], user['name'], user['city'])

@app.route('/register',methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate():
        pw_hash = bcrypt.generate_password_hash(form.password.data) #Hash the inputted pw
        db.insert_db('insert into users (username, password, email, name, city, role) values (?,?,?,?,?,?)',
                [form.username.data,
                pw_hash, #drop in the hashed password
                form.email.data,
                form.name.data,
                form.city.data,
                1],True)
        flash("User: " + form.username.data + " has been successfully registered!")
        user = db.pullUserObj(form.username.data, form.password.data) 
        if login_user(user,0): #Everything looks good attempt login.
            return redirect('/')
        else:
            flash("Could Not Login After Registering. Try manually logging in.")    
        return redirect('/login') #Dump them back to login, maybe this'll work?
    return render_template('register.html', title='Register', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')
