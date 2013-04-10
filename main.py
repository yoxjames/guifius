#imports
from __future__ import with_statement
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
	abort, render_template, flash
from contextlib import closing

#config
DATABASE = '/tmp/gus.db'
DEBUG = True
SECRET_KEY = 'devkey'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)

def init_db():
	with closing(connect_db()) as db:
		with app.open_resource('schema.sql') as f:
			db.cursor().executescript(f.read())
		db.commit()

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_request():
	g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
	g.db.close()

@app.route('/')
def explore():
	cur = g.db.execute('select name from nodes order by id')
	nodes = [dict(name=row[0]) for row in cur.fetchall()]
	return render_template('explore.html', nodes=nodes)

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
	error = None
	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME']:
			error = 'Invalid Username'
		elif request.form['password'] != app.config['PASSWORD']:
			error = 'Invalid Password'
		else:
			session['logged_in'] = True
			flash('Success')
			return redirect(url_for('explore'))
	return render_template('login.html', error=error)

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('Logged out')
	return redirect(url_for('explore'))

if __name__ == "__main__":
    app.run()
