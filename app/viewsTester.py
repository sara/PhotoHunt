from flask import Flask, request
from flask_pymongo import PyMongo
from twilio import twiml
from clarifai import rest
from clarifai.rest import ClarifaiApp, Image as ClImage
import json


app = Flask (__name__)
app.config['MONGO_DBNAME'] = 'photohunt'
app.config['MONGO_URI'] = 'mongodb://merp:derp@ds149258.mlab.com:49258/photohunt'
mongo = PyMongo(app)
globalRank = 1;

def main():
	checkPhoto('https://s3.amazonaws.com/clarifai-api/img/prod/f33f418d1bca40a79afaf91896caea67/a8b54c71163a4a61aa50bc2b16e95643.jpeg', 'baby')

def checkPhoto(pictureURL, tag):
	resp = twiml.Response()
	photoApp = ClarifaiApp()
	#all concepts attached to the item specified in photo database (i.e. answer key)
	with app.app_context():
		conceptGoals = mongo.db.photoGoals.find_one({"item":tag})
	model = photoApp.models.get(tag)
	image = ClImage(url='https://samples.clarifai.com/metro-north.jpg')
	#all data associated with each concept: id, name, appid, and value
	predictionData = model.predict([image])['outputs'][0]['data']['concepts']
	#['outputs']['data']['concepts']
	#predictionData = predictionData.replace("'", '"')
	#dataDict = json.loads(predictionData)
	#concepts = predictionData.get('outputs')
	print(predictionData)
	#userConcepts = []
	#for x in predictionData:
	#	userConcepts.append(x[1])
	#all concepts included in user's photo
	#conceptsPresent = conceptGoals.intersection(userConcepts)
	#numbers = []
	#for x in conceptsPresent:
		#threshold for approval is 51%
	#	probability = predictionData["value"]
	#	if probability > 0.5:
	#		numbers.append(probability)
	#if numbers.length > 2:
	#	return True
	#else:
	#	return False

def updateProfile(phoneNumber, tag):
	mongo.db.users.update_one(
		{"phoneNumber":phoneNumber,
		 "item":tag},
		{	#mark specified item as having been found; increment total number of items found in user profile
			'$set': {"scoresheet.$.found":true},
			'$inc': {"numFound": 1}
		})
	#check if user is done
	if mongo.db.users.find_one({"phoneNumber":phoneNumber})["numFound"] == 5:
		globalRank += 1
		return ('Good job, looks like you\'re done! You #' + globalRank-1 + ' to finish!')
	else:
		return ('Way to go! Your score has been adjusted')
		

if __name__ == '__main__':
	main()