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

login_manager = LoginManager()

login_manager.anonymous_user = Anonymous
login_manager.login_view = "login"
login_manager.login_message = "Please log in to access this page."
login_manager.refresh_view = "reauth"

login_manager.setup_app(app)

def query_db(query, args=(), one=False):
    cur = g.db.execute(query,args)
    rv = [dict((cur.description[idx][0], value)
        for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv

def pullUserObj(username, password): 
    user = query_db('select * from users where username = ? and password = ?'
            , [username, password], one=True)
    if user is None: #Username or password incorrect
        return None
    return User(user['id'], user['username'], user['password'], user['name'], user['city'])

def curUsername(id):
    if (id is None):
        return "ERROR: Invalid Query"
    else:
        name = query_db('select username from users where id = ?', [id], one=True)
        if name is None:
            return "Invalid ID"
        return name['username']

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
        curUser = curUsername(curUser)
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
        
        user = pullUserObj(username, password)
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
    user = query_db('select * from users where id = ?', [id], one=True)
    g.db.close()
    return User(user['id'], user['username'], user['password'], user['name'], user['city'])

@app.route('/register',methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        g.db.execute('insert into users (username, password, email, name, city, role) values (?,?,?,?,?,?)',
                [form.username.data,
                form.password.data,
                form.email.data,
                form.name.data,
                form.city.data,
                1])
        g.db.commit()
        flash("User Successfully Registered!")
        return redirect('/')
    return render_template('register.html', title='Register', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')
