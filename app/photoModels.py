import os
from glob import glob
from clarifai import rest
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
from pymongo import MongoClient

imagePaths = ['dogInStroller', 'happyCouple', 'stopSign', 'stuffedAnimal', 'baby'] 
connection = MongoClient ("mongodb://merp:blackjack10@ds149258.mlab.com:49258/photohunt")
db = connection.photoHunt


def main():
	photoApp = ClarifaiApp()
	#go through each search concept folder
	for searchItem in imagePaths:
		path = './pictures/' + searchItem
		collection = make_photo_collection
		#photoApp.inputs.bulk_create_images(collection)
		#make_and_train(searchItem)

def make_photo_collection(path):
	for path in glob (os.path.join(path, '*.jpg')):
			photoConcepts = db.photoGoals.find({item: searchItem}, {concepts: 1})
			for item in photoConcepts:
				print item			
			photo = ClImage(filename=path, concepts = db.photoGoals.find({item: searchItem}, {concepts: 1}))
			photoCollection.append(photo)
	return photoCollection

def make_and_train(model_id):
	setConcepts = db.photoGoals.find({item: searchItem}, {concepts: 1})
	model = photoApp.models.create (model_id, concepts = setConcepts)

if __name__ == '__main__':
	main()

