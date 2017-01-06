import os
from glob import glob
from clarifai import rest
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
#from app import flaskApp, mongo
from flask import Flask
from flask_pymongo import PyMongo

flaskApp = Flask(__name__)
flaskApp.config['MONGO_DBNAME'] = 'photohunt'
flaskApp.config['MONGO_URI'] = 'mongodb://merp:derp@ds149258.mlab.com:49258/photohunt'
mongo = PyMongo(flaskApp)


#connection = MongoClient('mongodb://merp:blackjack10@ds149258.mlab.com:49258/photohunt')
#db = connection['photohunt']


def main():
	photoApp = ClarifaiApp()
	imagePaths = ['dogInStroller', 'happyCouple', 'stopSign', 'stuffedAnimal', 'baby'] 

		#collection = make_photo_collection(path, searchItem)
	
	#go through each search concept folder
	for searchItem in imagePaths:
		path = './pictures/' + searchItem
		photoCollection = make_photo_collection(path, searchItem)
		photoApp.inputs.bulk_create_images(photoCollection)
		#make_and_train(searchItem)

def make_photo_collection(path, searchItem):
	photoCollection = []
	for path in glob (os.path.join(path, '*.jpg')):
		#with flaskApp.app_context():
		photo = ClImage(filename=path, 
		concepts = ['happy'])

			#concepts = list(mongo.db.photoGoals.find( {"item": searchItem}, {"concepts": 1} )))
		photoCollection.append(photo)
	return photoCollection

def make_and_train(model_id):
	setConcepts = db.photoGoals.find({item: searchItem}, {concepts: 1})
	model = photoApp.models.create (model_id, concepts = setConcepts)

if __name__ == '__main__':
	main()

