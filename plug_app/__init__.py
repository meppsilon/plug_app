import os
import sys
import sqlite3

from flask import Flask, render_template, g
from contextlib import closing

app = Flask(__name__)
app.config.from_object('config.BaseConfiguration')

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

def init_db():
	with closing(connect_db()) as db:
		with app.open_resource('schema.sql', mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()

@app.before_request
def before_request():
	g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
	db = getattr(g, 'db', None)
	if db is not None:
		db.close()

import plug_app.views 
import plug_app.users.views