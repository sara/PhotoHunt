import os
from glob import glob
from clarifai import rest
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
#from app import flaskApp, mongo
from flask import Flask
from flask_pymongo import PyMongo
from bson.json_util import dumps
import json

flaskApp = Flask(__name__)
flaskApp.config['MONGO_DBNAME'] = 'photohunt'
flaskApp.config['MONGO_URI'] = 'mongodb://merp:derp@ds149258.mlab.com:49258/photohunt'
mongo = PyMongo(flaskApp)


#connection = MongoClient('mongodb://merp:blackjack10@ds149258.mlab.com:49258/photohunt')
#db = connection['photohunt']


def main():
	photoApp = ClarifaiApp()
	imagePaths = ['dogInStroller', 'happyCouple', 'stopSign', 'stuffedAnimal', 'baby'] 
	#go through each search concept folder
	for searchItem in imagePaths:
		#path = './pictures/' + searchItem
		#photoCollection = make_photo_collection(path, searchItem)
		#photoApp.inputs.bulk_create_images(photoCollection)
		make_and_train(searchItem, photoApp)

def make_photo_collection(path, searchItem):
	photoCollection = []
	for path in glob (os.path.join(path, '*.jpg')):
		with flaskApp.app_context():
			raw = mongo.db.photoGoals.find_one({"item": searchItem})["concepts"]
			polished = [str(r) for r in raw]
			photo = ClImage(filename=path, concepts = polished)
			#print cleanConcepts
			photoCollection.append(photo)
	return photoCollection

def make_and_train(model_id, app):
	with flaskApp.app_context():
		raw = mongo.db.photoGoals.find_one({"item": model_id})["concepts"]
		polished = [str(r) for r in raw]
	model =  app.models.create (model_id, concepts = polished)

if __name__ == '__main__':
	main()

