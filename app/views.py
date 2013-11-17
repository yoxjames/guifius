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
map_db = Map_db()
network_db = Network_db()
device_db = Device_db()
point_db = Point_db()
user_db = User_db()
polygon_db = Polygon_db()


''' 
'  BEGIN AJAX LISTENERS
''' 


'''
LISTENER
/ajax/add_network
Parameters:
name: Name of the Network
Rules:
<NONE> TODO (This probably needs some kind of security)
'''
@app.route('/ajax/add_network', methods=['POST'])
def add_network():
    if request.method == 'POST':
        network_id = network_db.add_network(
            request.json['name'],
            request.json['type_val'],
            request.json['phase_type_val'],
            current_user.get_id() or 0)
        return str(network_id);
    else:
        return ""

'''
LISTENER
/ajax/add_polygon
Parameters:
network_id: ID of the network we are adding a polygon to.
polygon_json: JSON representing the polygon
Rules:
network_id > 0
polygon_json != None
network_id must be a network that is related to the current user
'''

@app.route('/ajax/add_polygon', methods=['POST'])
def add_polygon():
    if request.method == 'POST':
        
        polygon_id = polygon_db.add_polygon(
                request.json['data'])
        network_id = network_db.add_network_polygon(
                request.json['network_id']
                , polygon_id)

        return "SUCCESS"
    return ""

@app.route('/ajax/add_device', methods=['POST'])
def add_device():
    if request.method == 'POST':

        ## Add the point
        point_id = point_db.add_point(
                request.json['lat'],
                request.json['lon'])

        ## Add the device over the point
        device_id = device_db.add_device(
                request.json['name'],
                request.json['type_val'],
                point_id,
                request.json['polarization_type_val'],
                request.json['status_type_val'],
                request.json['network_id']) # For the reltn


        return "SUCCESS"
    else:
        return ""

@app.route('/ajax/get_devices_for_network', methods=['POST'])
def get_devices_for_network():
    if request.method == 'POST':
        return json.dumps(device_db.get_devices_for_network(request.json['network_id']))
    else:
        return ""


@app.route('/ajax/commit_network', methods=['POST'])
def commit_network():
    if request.method == 'POST':
        network_db.update_network(
                request.json['network_id'],
                request.json['name'],
                request.json['type_val'],
                request.json['phase_type_val'])
        return "SUCCESS"
    return ""

''' 
'  END AJAX LISTENERS 
'''

'''
' BEGIN SPECIAL HOOKS
'''

@login_manager.user_loader
def load_user(id):
    return user_db.get_user(id)

'''
' END SPECIAL HOOKS
'''

'''
' BEGIN HTTP LISTENERS
'''

@app.route('/')
def explore():
    curUser = ""
    
    overlay_data=map_db.get_default_json()
    overlay_data_str=json.dumps(overlay_data)

    overlay_device = []

    
    for network in overlay_data:
        overlay_device.append(map_db.get_devices_json(network['id']))

    overlay_device_str = json.dumps(overlay_device)

    if current_user.is_authenticated():
        current_username = user_db.get_username(current_user.get_id())
    else:
        current_username = "not logged in"

    
    #nodes = data.query_db("select * from point",[]) comment: fix
    nodes = []
    
    # Mode: 1 is for EXPLORE mode.
    return render_template('explore.html', \
            overlay_data=overlay_data_str, \
            overlay_device=overlay_device_str, \
            current_username=current_username, mode=1)

@app.route('/build', methods=['POST', 'GET'])
def build():
    curUser= ""
    if current_user.is_authenticated():
        current_username = user_db.get_username(current_user.get_id())
    else:
        # NOT MEANT FOR PRODUCTION
        current_username = "not logged in"
    overlay_data=map_db.get_default_json()
    overlay_data_str=json.dumps(overlay_data)
    
    overlay_device = []

    for network in overlay_data:
        overlay_device.append(map_db.get_devices_json(network['id']))

    overlay_device_str = json.dumps(overlay_device)


    
    # Mode: 2 is for BUILD mode.
    return render_template('explore.html', \
            overlay_data=overlay_data_str, \
            overlay_device=overlay_device_str, \
            networks=json.dumps(user_db.get_my_networks(current_user.get_id())), \
            current_username=current_username, mode=2) 

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

'''
' END HTTP LISTENERS
'''
