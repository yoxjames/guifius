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

import obj

from werkzeug.contrib.cache import SimpleCache

''' INITIALIZE ALL OBJECTS '''
# Global
@app.before_first_request
def cache_code_class():
    obj.cache.set('CODE_CLASS',CODE_CLASS(), timeout=None)

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
connection_db = Connection_db()


'''
'  BEGIN HELPER METHODS
'''

def sync():
    online_networks=map_db.get_default_json()
    
    # Create JSON Template:
    map_data = \
    {
        'online_networks' : [],
        'in_progress_networks' : [],
        'planning_networks' : [],
        'fun_networks' : []
    }


    # Populate Template:
    

    for network in online_networks:
        device_list = []

        device_query = map_db.get_devices_json(network['id'])
        
        for device in device_query:
            connection_list = []
            connection_list = connection_db.get_device_connections(device['id'])
            device_list.append \
            (
                    {
                        'device': 
                        {
                            'lat': device['lat'],
                            'lon': device['lon'],
                            'name': device['name'],
                            'id': device['id']
                        },
                        'connections': connection_list
                    }
            )



        map_data['online_networks'].append \
        (
                { 
                    'id': network['id'],
                    'name': network['name'],
                    'data': network['data'],
                    'type_val': "ONLINE",
                    'devices' : device_list
                }
        )

    return json.dumps(map_data)





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

        return json.dumps("SUCCESS")
    return ""

@app.route('/ajax/add_device', methods=['POST'])
def add_device():
    if request.method == 'POST':


        ## Check if point already exists, if so use update logic 
        # else use insertion logic.
            # Update point
        if (request.json['new'] == "FALSE"):
            point_id = device_db.get_point_id(request.json['device_id'])
            point_db.move_point( #Handle Point Relocation
                    point_id,
                    request.json['lat'],
                    request.json['lon'])

            device_db.update_device(
                    request.json['device_id'], 
                    request.json['name'],
                    request.json['type_val'],
                    request.json['polarization_type_val'],
                    request.json['status_type_val'],
                    request.json['azimuth'] or None,
                    request.json['elevation'] or None)
            
        else:
            # Add new point
            point_id = point_db.add_point(
                    request.json['lat'],
                 request.json['lon'])

            ## Add the device over the point
            device_id = device_db.add_device(
                    request.json['name'],
                    "UNKNOWN",
                    #request.json['type_val'],
                    point_id,
                    "UNKNOWN",
                    #request.json['polarization_type_val'],
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

@app.route('/ajax/get_device_info', methods=['POST'])
def get_device_info():
    if request.method == 'POST':
        return json.dumps(device_db.get_device(request.json['device_id']))


@app.route('/ajax/connect_devices', methods=['POST'])
def connect_devices():
    if request.method == 'POST':
        target_point_id = device_db.get_point_id(request.json['device_b_id'])

        return json.dumps(connection_db.connect_devices(
                request.json['device_a_id'],
                target_point_id,
                request.json['type_val'],
                request.json['active'],
                request.json['device_b_id'],
                request.json['bandwidth']))

@app.route('/ajax/inactivate_connection', methods=['POST'])
def inactivate_connection():
    if request.method == 'POST':
        return connection_db.inactivate(
                request.json['id'])

@app.route('/ajax/activate_connection', methods=['POST'])
def activate_connection():
    if request.method == 'POST':
        return connection_db.activate(
                request.json['id'])


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
    map_data = sync()

    if current_user.is_authenticated():
        current_username = user_db.get_username(current_user.get_id())
    else:
        current_username = "not logged in"
    
    # Mode: 1 is for EXPLORE mode.
    return render_template('explore.html', \
            map_data=map_data, \
            code_cache=json.dumps(obj.cache.get('CODE_CLASS').E), \
            current_username=current_username, mode=1)

@app.route('/build', methods=['POST', 'GET'])
def build():
    curUser= ""
    if current_user.is_authenticated():
        current_username = user_db.get_username(current_user.get_id())
    else:
        # NOT MEANT FOR PRODUCTION
        current_username = "not logged in"

    map_data = sync()
    
    # Mode: 2 is for BUILD mode.
    return render_template('explore.html', \
            map_data = map_data, \
            code_cache=json.dumps(obj.cache.get('CODE_CLASS').E), \
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
