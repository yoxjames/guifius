from flask.ext.login import UserMixin, AnonymousUser
from code_val import * #Probably should make this a list? idk....
from db import Database
from flaskext.bcrypt import Bcrypt
from app import app
from flask import g

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

class Anonymous(AnonymousUser):
    name = u"Anonymous"

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
        return ""

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
        network_id = \
        self.insert_db('insert into network (name, type_val, phase_type_val) values (?,?,?)',
                [name, type_val, phase_type_val], True)
        reltn_type_val = g.CODE_CLASS.RELATION.A_NETWORK_B_PERSON
        self.add_reltn(network_id, owner_id, reltn_type_val)
        return network_id

    def get_devices(self, id):
        return ""

    def get_network_polygon(self, id):
        return ""

    def add_network_polygon(self, id):
        return ""

class Polygon_db(Database):
    
    def add_polygon(self, json):
        polygon_id = \
        self.insert_db('insert into object (type_val,data) values (?,?)',
                [g.CODE_CLASS.OBJECT_TYPE.POLYGON, json], True)
        return polygon_id


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
    def add_device(self,point_id):
        return 0

    '''
    add_device()
    TODO
    Adds a device AND a point
    Parameters: 
    None
    Returns:
    device_id: ID of the Device added
    '''
    def add_device(self):
        return 0

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
        return 0
    
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



