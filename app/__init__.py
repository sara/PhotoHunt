from flask import Flask
from flask.ext.pymongo import PyMongo

flaskApp = Flask(__name__)
flaskApp.config['MONGO_DBNAME'] = 'photohunt'
flaskApp.config['MONGO_URI'] = 'mongodb://merp:derp@ds149258.mlab.com:49258/photohunt'
#changed from PyMongo(app)
mongo = PyMongo(flaskApp)
