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
login_manager.login_message = u"Please log in to access this page."
login_manager.refresh_view = "reauth"

login_manager.setup_app(app)

'''
Currently not operational
'''
def pullUserObj(username): 
    cur = g.db.execute("select * from users where username = ?", [username])
    user = [dict(name=row[0]) for row in cur.fetchall()]
    return User(user.id, user.username, user.password, user.name, user.city)

@app.before_request
def before_request():
	g.db = db.connect_db()

@app.teardown_request
def teardown_request(exception):
	g.db.close()

@app.route('/')
def explore():
	cur = g.db.execute('select name from nodes order by id')
	nodes = [dict(name=row[0]) for row in cur.fetchall()]
	return render_template('explore.html', nodes=nodes)

@app.route('/build')
def build():
	cur = g.db.execute('select name from nodes order by id')
	nodes = [dict(name=row[0]) for row in cur.fetchall()]
	return render_template('build.html', nodes=nodes)

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
        #if username == "yoxjames": #Query Database
        remember = form.remember_me.data
        if login_user(pullUserObj(username), remember=remember):
            flash("Logged in")
            return redirect('/')
        else:
            flash("Login Failed")    
        return redirect('/login')
    return render_template('login.html', title= 'Sign In', form = form)


@login_manager.user_loader
def load_user(id):
    cur = g.db.execute("select * from users u where u.id = ?",[id])
    u = [dict(name=row[0]) for row in cur.fetchall()]
    return User(u.id, u.username, u.password, u.name, u.city, u.role)

@app.route('/register',methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        g.db.execute('insert into users (username, password, name, city, role) values (?,?,?,?,?)',
                [form.username.data,
                form.password.data,
                form.name.data,
                form.city.data,
                1])
        g.db.commit()
        flash("User Successfully Registered!")

        return redirect('/')
    return render_template('register.html', title='Register', form=form)

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('Logged out')
	return redirect(url_for('explore'))