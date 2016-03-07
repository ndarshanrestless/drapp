# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
         abort, render_template, flash, Response
from contextlib import closing
import ipdb
from flask.json import jsonify

# create our little application :)
app = Flask(__name__)
app.config.update(dict(
    DATABASE='/ebs/tmp/flaskr.db',
    DEBUG=True,
    SECRET_KEY='restless123',
    USERNAME='bandit',
    PASSWORD='restless',
))
app.config.from_object(__name__)


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
        return g.sqlite_db


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.route('/', strict_slashes=False)
def root_page():
    return Response("What are you looking at?", 200)


@app.route('/test', methods=['GET'])
def show_entries():
    cur = g.db.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    j = {'key1': 'value1', 'key2': 'value2'}
    return jsonify(j)


@app.route('/createuser', methods=['POST'])
def create_user():
    """                                                                                                           {                                                                                                            "username": "naren",                                                                                         "password": "welcome",                                                                                       "doctor-type": "Some Dr speciality"                                                                          }                                                                                                            """
    jd = request.get_json()

    db = get_db()
    db.execute('insert into entries (title, text) values (?, ?)',
               [jd['username'], jd['password']])
    db.commit()
return Response("Created user succesfully!", 200)


@app.route('/showusers, methods=['GET']')
def show_user_entries():
    cur = g.db.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
return jsonify(entries)


@app.route('/add', methods=['POST'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)


'''
That way someone can set an environment variable called FLASKR_SETTINGS
to specify a config file to be loaded which will then override the default
values. The silent switch just tells Flask to not complain if no such
 environment key is set.

app.config.from_envvar('FLASKR_SETTINGS', silent=True)
'''
