#imports
from __future__ import with_statement
from code_val import *
import json
from flask import Flask, request, session, g, redirect, url_for, \
	abort, render_template, flash
from forms import *
from flask.ext.login import (LoginManager, current_user, login_required,
                            login_user, logout_user, UserMixin, AnonymousUser,
                            confirm_login, fresh_login_required)
from app import app
from models import *
from flaskext.babel import Babel

''' INITIALIZE ALL OBJECTS '''
# Global
@app.before_request
def before_request():
    g.CODE_CLASS = CODE_CLASS()

# Local
login_manager = LoginManager()
login_manager.anonymous_user = Anonymous
login_manager.login_view = "login"
login_manager.login_message = "Please log in to access this page."
login_manager.refresh_view = "reauth"
login_manager.setup_app(app)

bcrypt = Bcrypt(app)
babel = Babel(app)
network_db = Network_db()
user_db = User_db()

''' 
'  BEGIN AJAX LISTENERS
''' 

@app.route('/ajax/add_network', methods=['POST'])
def add_network():
    if request.method == 'POST':
        network_db.add_network(
                request.json['name'],
                request.json['type_val'],
                request.json['phase_type_val'],
                0)
        return json.dumps("S");

@app.route('/ajax/add_poly', methods=['POST'])
def add_poly():
    if request.method == 'POST':
        return ""

@app.route('/ajax/add_node', methods=['POST'])
def add_node():
    return ""

''' 
'  END AJAX LISTENERS 
'''

@app.route('/')
def explore():
    curUser = ""
    if current_user.is_authenticated():
        curUser = user_db.get_username(current_user.get_id())
    
    #nodes = data.query_db("select * from point",[]) comment: fix
    nodes = []
    
    # Mode: 1 is for EXPLORE mode.
    return render_template('explore.html', \
            nodes=json.dumps(nodes), \
            curUser= curUser, mode=1)

@app.route('/build', methods=['POST', 'GET'])
def build():
    curUser= ""
    if current_user.is_authenticated():
        curUser = user_db.get_username(current_user.get_id())

    
    #nodes = data.query_db("select * from point",[],one=False) comment: fix
    nodes = []
    
    # Mode: 2 is for BUILD mode.
    return render_template('explore.html', \
            nodes=json.dumps(nodes), \
            curUser=curUser, mode=2) 

@app.route('/contact')
def contact():
    curUser = ""
    if current_user.is_authenticated():
        curUser = user_db.get_username(current_user.get_id())

    return render_template('base.html', curUser=curUser)

@app.route('/about')
def about():
    curUser = ""
    if current_user.is_authenticated():
        curUser = user_db.get_username(current_user.get_id())

    return render_template('base.html', curUser=curUser)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated():
       return redirect('/') 

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember_me.data
        user = user_db.authenticate_user(username, password)
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
    return user_db.get_user(id)

@app.route('/register',methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = user_db.add_user(form.username.data, form.password.data, form.email.data)
        flash("User: " + form.username.data + " has been successfully registered!")
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
