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

class Network_db(Database):

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


class User_db(Database):

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
            name = self.query_db('select username from users where id = ?', [id], one=True)
            if name is None:
                return "Invalid ID"
            return name['username']

    def get_user(self, id):
        if (id is None):
            raise "Hell"
        else:
            user = self.query_db('select * from users where id = ?', [id], one=True)
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
        name = self.query_db('select username from users where username = ?', [username], one=True)
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
        email = self.query_db('select email from users where email = ?', [email], one=True)
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
    '''
    def add_user(self, username, password, email):
        # Generate the hash
        pw_hash = bcrypt.generate_password_hash(password) #Hash the inputted pw
        self.insert_db('insert into users (username, password, email, type_val) values (?,?,?,?)',
                [username,
                pw_hash, #drop in the hashed password
                email,
                1],
                True)
        return self.authenticate_user(username,password) 



