import sqlite3
from contextlib import closing
from app import app

class Database:    
    '''
    __init__
    Default Constructor
    Pass refresh=True to drop all tables and rebuild schema
    '''
    def __init__(self, refresh=False):
        if (refresh):
            self.refresh()

    '''
    connect
    Initializes the connection to the database. Generally,
    this should only be called once when the application begins
    '''
    def connect(self):
        return sqlite3.connect(app.config['DATABASE'])
    
    '''
    refresh
    Creates a database and sets up the schema and injects all starter
    data needed to run this application.
    '''
    def refresh(self):
        with closing(self.connect()) as db:
            with app.open_resource('schema.sql') as f:
                db.cursor().executescript(f.read())
            db.commit()
            db.close()
 
    '''
    query_db
    Helper function designed to query the db using
    a SQL statement as query.
    Parameters:
    self
    query: string that represents SQL query
    args: arguments for the string query
    one: boolean, true=only one row returned.
    '''

    def query_db(self, query, args=(), one=False):
        cur = self.connect().execute(query,args)
        rv = [dict((cur.description[idx][0], value)
            for idx, value in enumerate(row)) for row in cur.fetchall()]
        cur.close()
        return (rv[0] if rv else None) if one else rv

    '''
    insert_db
    Helper function that executes a SQL insert statement.
    If commit=True it commits
    Parameters:
    self
    query: string representing the SQL query
    args: arguments to be placed into the query string as []
    commit: True auto commits... not sure why anyone would use False....
    Returns: Primary Key of the row inserted.
    '''
    def insert_db(self, query, args=(), commit=True):
        cur = self.connect().cursor().execute(query, args)
        if (commit):
            cur.connection.commit();
        return cur.lastrowid
    
    '''
    add_reltn
    This function is used to add relations to the database.
    Since this is used by all inheriting objects it makes sense
    to implement it at the Database level.
    Parameters:
    self
    a_id: Primary Key of A
    b_id: Primary Key of B
    type_val: Type code of relationship
    '''
    def add_reltn(self, a_id, b_id, type_val):
        self.insert_db('insert into relation (a_id, b_id, type_val) values (?,?,?)',
                [a_id, b_id, type_val], True)

    '''
    update_db
    TODO NOT YET COMPLETED BUT NEEDS TO BE IMPLEMENTED!
    '''
