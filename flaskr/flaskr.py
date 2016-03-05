# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
         abort, render_template, flash
from contextlib import closing


# configuration
DATABASE = '/ebs/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'restless123'
USERNAME = 'bandit'
PASSWORD = 'restless'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)


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


if __name__ == '__main__':
    app.run()

'''
That way someone can set an environment variable called FLASKR_SETTINGS
to specify a config file to be loaded which will then override the default
values. The silent switch just tells Flask to not complain if no such
 environment key is set.

app.config.from_envvar('FLASKR_SETTINGS', silent=True)
'''
