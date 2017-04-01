import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restless import APIManager


app = Flask(__name__)

path = os.path.dirname(os.path.abspath(__file__))

config_file = os.path.join(path, '../config.cfg')
app.config.from_pyfile(config_file)
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

'''Read the secret key from file is it exist or generate
   a secret random key for the session and write in the file'''
secret_file = os.path.join(path, '../secret.key')
if os.path.isfile(secret_file):
    with open(secret_file, 'r') as fh:
        app.secret_key = fh.read()
else:
    app.secret_key = os.urandom(128)
    with open(secret_file, 'w') as fh:
        fh.write(app.secret_key)

db = SQLAlchemy(app)

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    pets = db.relationship('Pet', backref='owner', lazy='dynamic')

class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    owner_id = db.Column(db.Integer, db.ForeignKey('person.id'))

manager = APIManager(app, flask_sqlalchemy_db=db)

manager.create_api(Person, results_per_page=None, methods=['GET', 'POST', 'DELETE', 'PATCH'])
manager.create_api(Pet, results_per_page=None, methods=['GET', 'POST', 'DELETE', 'PATCH'])
