#imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
	abort, render_template, flash

#config
DATABASE = 'tmp/gus.db'
DEBUG = True
SECRET_KEY = 'devkey'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)

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

if __name__ == "__main__":
    app.run()


@app.before_request
def before_request():
	g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
	g.db.close()
