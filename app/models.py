import queries

from flask.ext.login import UserMixin 
from code_val import * #Probably should make this a list? idk....
from db import Database
from flask.ext.bcrypt import Bcrypt
from app import app

import obj

from werkzeug.contrib.cache import SimpleCache


bcrypt = Bcrypt(app)


class User(UserMixin):
    
    def __init__(self, id, username, password, email, name=None, city=None):
        self.id = id
        self.username = username
        self.password = password
        self.email = email
        self.name = name
        self.city = city
        self.role = 1

    def is_authenticated(self):
        return True

    def is_active(self):
        if self.role == 0:
            return False
        else:
            return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.username)

class Network:
    def __init__(self, id, name, type_val, phase_type_val, geometry_obj=None, nodes=[]):
        self.id = id
        self.type_val = type_val
        self.phase_type_val = phase_type_val
        self.geometry_obj = geometry.obj #Can be null
        self.nodes = nodes #Can be null

class Map_db(Database):
    
    def __init__(self):
        self.network_db = Network_db()

    def get_default_json(self):
        return self.query_db(
                queries.get_networks_main, 
                [
                    obj.cache.get('CODE_CLASS').I['NET_PHASE_TYPE']['PLANNED'],
                    obj.cache.get('CODE_CLASS').I['NET_PHASE_TYPE']['IN_PROGRESS'],
                    obj.cache.get('CODE_CLASS').I['NET_PHASE_TYPE']['ONLINE']
                ])

    def get_devices_json(self, network_id):
        return self.query_db(queries.get_devices_for_network_json, 
                [
                    network_id,
                    obj.cache.get('CODE_CLASS').I['RELATION']['A_NETWORK_B_DEVICE'],
                    obj.cache.get('CODE_CLASS').I['NET_PHASE_TYPE']['ONLINE']
                    
                ],
                one=False)

class Network_db(Database):

    def __init__(self):
        self.device_db = Device_db()
        self.polygon_db = Polygon_db()

    '''
    add_network
    Adds a new network to the Database
    Parameters:
    self
    name (string): name of network
    type_val (type val): Type of network
    phase_type_val (type_val): Phase of Network (level of completion)
    '''
    def add_network(self, name, type_val, phase_type_val, owner_id):

        # Parse TYPES
        type_val = obj.cache.get('CODE_CLASS').I['NET_TYPE'][type_val]
        phase_type_val = obj.cache.get('CODE_CLASS').I['NET_PHASE_TYPE'][phase_type_val]

        # SQL
        network_id = \
        self.insert_db(queries.insert_network,[name, type_val, phase_type_val], True)
        reltn_type_val = obj.cache.get('CODE_CLASS').I['RELATION']['A_NETWORK_B_PERSON']
        self.add_reltn(network_id, owner_id, reltn_type_val)
        return network_id

    def update_network(self, network_id, name, type_val, phase_type_val):
        # Parse TYPE VALS
        type_val = obj.cache.get('CODE_CLASS').I['NET_TYPE'][type_val]
        phase_type_val = obj.cache.get('CODE_CLASS').I['NET_PHASE_TYPE'][phase_type_val]

        # Run SQL
        self.insert_db(queries.update_network, 
                [name,type_val,phase_type_val, network_id])

    def get_devices(self, id):
        devices = self.query_db(queries.get_devices,
                [id, obj.cache.get['CODE_CLASS'].I['RELATION']['A_NETWORK_B_DEVICE']])
        return devices

    def get_network_polygon(self, id):
        poly = self.query_db(queries.get_network_polygon, [id], one=True)
        return poly['data']

    def add_network_polygon(self, id, polygon_obj_id):
        self.insert_db(queries.add_polygon_to_network, [polygon_obj_id, id], True)
        return True
        

class Polygon_db(Database):
    
    def add_polygon(self, json):
        polygon_id = \
        self.insert_db('insert into object (type_val,data) values (?,?)',
                [obj.cache.get('CODE_CLASS').I['OBJECT']['POLYGON'], json], True)
        return polygon_id


class Connection_db(Database):

    def __init__(self):
        self.stub = "this is pointless"


    def connect_devices(
            self, 
            device_a_id, 
            target_point_id,
            type_val, 
            active,
            device_b_id=None, 
            bandwidth=None):

        type_val = obj.cache.get('CODE_CLASS').I['CONNECTION_TYPE'][type_val]

        connection_id = self.insert_db(
                queries.connect_devices,
                [
                    type_val,
                    device_a_id,
                    device_b_id,
                    target_point_id,
                    active,
                    bandwidth
                ],
                True)
        return connection_id
                    
    def inactivate_connection(self,id):
        return self.insert_db(queries.inactivate_connection,[id],True)

    def activate_connection(self,id):
        return self.insert_db(queries.activate_connection,[id],True)

    def get_device_connections(self,device_id):
        raw_output = self.query_db(
                queries.get_device_connections,
                [device_id],
                one=False)
        for device in raw_output:
            device['type_val'] = obj.cache.get('CODE_CLASS').VAL[device['type_val']]

        return raw_output
    


class Device_db(Database):
    
    def __init__(self):
        self.point_db = Point_db()

    '''
    add_device(point_id)
    TODO
    Adds a device on to an existing point ID.
    Parameters:
    point_id: Point we are adding the device to
    Returns:
    device_id: ID of the device added
    '''
    def add_device(
            self, 
            name, 
            type_val, 
            point_id, 
            polarization_type_val, 
            status_type_val, 
            network_id, 
            azimuth=None, 
            elevation=None):

        # Parse Code Types

        type_val = obj.cache.get('CODE_CLASS').I['NET_TYPE'][type_val]
        status_type_val = obj.cache.get('CODE_CLASS').I['NET_PHASE_TYPE'][status_type_val]
        polarization_type_val = obj.cache.get('CODE_CLASS').I['POLARIZATION_TYPE'][polarization_type_val]

        device_id = \
                self.insert_db(
                        queries.add_device, 
                        [
                            name, 
                            type_val, 
                            point_id, 
                            azimuth, 
                            elevation, 
                            polarization_type_val,
                            status_type_val], True)


        self.add_reltn(
                network_id, 
                device_id, 
                obj.cache.get('CODE_CLASS').I['RELATION']['A_NETWORK_B_DEVICE']);



        return device_id

    '''
    add_device()
    TODO
    Adds a device AND a point
    Parameters: 
    None
    Returns:
    device_id: ID of the Device added
    
    def add_device(self):
        return 0
    '''


    def get_devices_for_network(self, network_id):
        return self.query_db(queries.get_devices_for_network, 
                [
                    obj.cache.get('CODE_CLASS').I['RELATION']['A_NETWORK_B_DEVICE'], 
                    network_id
                ],
                one=False)

    def get_device_on_point(self, point_id):
        return self.query_db(
                queries.get_device_on_point, 
                [point_id], 
                one=True)

    def name_exists(self, name):
        if (self.query_db(
            queries.pull_device_id_by_name,
            [name],
            one=True) is None):
            return False
        else:
            return True

    def get_device(self, id):
        device =  self.query_db(queries.get_device, [id], one=True)
        device['type_val'] = obj.cache.get('CODE_CLASS').VAL[device['type_val']]
        device['polarization_type_val'] = \
            obj.cache.get('CODE_CLASS').VAL[device['polarization_type_val']]
        # FIX: PHASE TYPE VAL NEEDED HERE!

        return device

    def get_point_id(self, id):
        return self.query_db(queries.get_point_id, [id], one=True)['point_id']

    def update_device(
            self, 
            id, 
            name, 
            type_val, 
            polarization_type_val, 
            status_type_val,  
            azimuth=None, 
            elevation=None):

        # Parse type vals
        type_val = obj.cache.get('CODE_CLASS').I['NET_TYPE'][type_val]
        polarization_type_val = \
            obj.cache.get('CODE_CLASS').I['POLARIZATION_TYPE'][polarization_type_val]
        status_type_val = obj.cache.get('CODE_CLASS').I['NET_PHASE_TYPE'][status_type_val]
        

        # Perform SQL
        self.insert_db(
                queries.update_device,
                [
                    name,
                    type_val,
                    polarization_type_val,
                    status_type_val,
                    azimuth,
                    elevation,
                    id
                ], 
                True)



class Point_db(Database):
    '''
    add_point
    Adds a point to the database
    Parameters:
    lat: latitude
    lon: longitude
    altitude: altitude (can be Null)
    seq: sequence (May not be used)
    Returns:
    Point ID of newly created point
    '''
    def add_point(self, lat, lon, altitude=None, seq=None):
        point_id = \
        self.insert_db('insert into point (lat,lon,altitude,seq) values (?,?,?,?)',
            [lat,lon,altitude,seq], True)
        return point_id

    '''
    move_point
    TODO
    '''
    def move_point(self,id,lat,lon):
        self.insert_db(
                queries.move_point,
                [lat,lon,id],
                True)
    
    '''
    delete_point
    TODO
    '''
    def delete_point(self,id):
        return 0

    '''
    get_point
    TODO
    Returns a Point object
    '''
    def get_point(self,id):
        return None



class User_db(Database):


    def __init__(self):
        self.network_db = Network_db()
        self.device_db = Device_db()
    '''
    authenticate_user
    Attempts to authenticate the user against the db with
    provided username and password.
    Parameters:
    self
    username (string): Username
    password (string): Password (NOT HASHED)
    '''
    def authenticate_user(self, username, password):
        user = self.query_db('select * from users where username = ?'
                , [username], one=True)
        if (user is None):
            return None
        elif (not bcrypt.check_password_hash(user['password'], password)):
            return None
        else:
            return User(user['id'], user['username'], user['password'], user['email'])

    '''
    get_username
    Grabs the username string from the database given the primary key of user
    Parameters:
    self
    id (int): Primary key of user who's username we want.
    '''
    def get_username(self, id):
        if (id is None):
            return "ERROR: Invalid Query"
        else:
            name = self.query_db('select username from users where id = ?', 
                    [id], one=True)
            if name is None:
                return "Invalid ID"
            return name['username']

    '''
    get_user
    Given an id this method returns a User object instance by 
    created from information on the db.
    Parameters:
    id: Primary Key of User
    '''
    def get_user(self, id):
        if (id is None):
            raise "Hell"
        else:
            user = self.query_db('select * from users where id = ?', 
                    [id], one=True)
            if user is None:
                return None
            return User(user['id'], user['username'], user['password'], user['email'])
            


    '''
    username_exists
    Checks whether a username is already in the database (should be unique)
    Parameters:
    self
    username (string): username we are checking if exists
    '''
    def username_exists(self, username):
        name = self.query_db('select username from users where username = ?', 
                [username], one=True)
        if name is None:
            return False
        else:
            return True

    '''
    email_exists
    Checks whether an email is already in the database (should be unique)
    Parameters:
    self
    email (string): email we are querying for in the db.
    '''
    def email_exists(self, email):
        email = self.query_db('select email from users where email = ?', 
                [email], one=True)
        if email is None:
            return False
        else:

            return True
    '''
    add_user
    Adds a user to the Database. This is used by the register view to
    add new users
    Parameters:
    self
    username (string): Username the user will use to log in.
    password (string): NOT HASHED Password. Hashing is done in this function
    email (string): User's email address to be stored in the db
    Returns:
    User: Object representing the User (see Class User)
    '''
    def add_user(self, username, password, email):
        # Generate the hash
        pw_hash = bcrypt.generate_password_hash(password) #Hash the inputted pw
        uid = self.insert_db('insert into users (username, password, email, type_val) values (?,?,?,?)',
                [username,
                pw_hash, #drop in the hashed password
                email,
                1],
                True)
        return self.get_user(uid)

    def get_my_networks(self, id):
        networks = self.query_db(
                queries.get_my_networks, 
                [
                    obj.cache.get('CODE_CLASS').I['RELATION']['A_NETWORK_B_PERSON'],
                    id]
                , 
                one=False)

        for n in networks:
            n['phase_type_val'] = obj.cache.get('CODE_CLASS').VAL[n['phase_type_val']]
            n['type_val'] = obj.cache.get('CODE_CLASS').VAL[n['type_val']]

        print networks
        return networks



