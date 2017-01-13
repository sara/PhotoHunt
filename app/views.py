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

@app.route('/sms', methods = ['POST'])
def validate():
	resp = twiml.Response()
	#grab all valid phone numbers from database
	userNums = mongo.db.users.count({"phoneNumber": request.form['From']})
	#grab # of items with the label specified by user
	photoGoals = mongo.db.photoGoals.count({"item":request.form['Body']})
	#validate that the number is in the game
	if userNums != 1:
		resp.message('Uh oh. Looks like this phone isn\'t part of the game!')
		return str(resp)
	#validate that jpg is attached
	elif int(request.form['NumMedia']) != 1:
		resp.message('Make sure you attach one picture')
		return str(resp)
	#verify this later	
	#elif str(request.form['MediaContentType0'])!='image/jpeg':
	#	resp.message('Pictures only please!')
	#	return str(resp)
	#validate that item specified is real
	elif photoGoals < 1:
		resp.message('Sure that\'s the right label?')
		return str(resp)
	else:
		#url of attached photo
		url = request.form['MediaUrl0']
		#item specified
		tag = request.form['Body']
		#match is valid
		if (checkPhoto(url, tag)):
			resp.message(updateProfile(request.form['From'], tag))
		#match is not valid
		else:
			resp.message('Sorry, that picture doesn\'t count')
		return str(resp)

def checkPhoto(pictureURL, tag):
	resp = twiml.Response()
	photoApp = ClarifaiApp()
	#all concepts attached to the item specified in photo database (i.e. answer key)
	conceptGoals = [str(x) for x in mongo.db.photoGoals.find_one({"item":tag})["concepts"]]
	model = photoApp.models.get(tag)
	image = ClImage(url = pictureURL)
	#all data associated with each concept: id, name, appid, and value
	predictionData = json.loads(str(model.predict([image])))['outputs']['data']['concepts']
	userConcepts = []
	for x in predictionData:
		userConcepts.append(x[1])
	#all concepts included in user's photo
	conceptsPresent = conceptGoals.intersection(userConcepts)
	numbers = []
	for x in conceptsPresent:
		#threshold for approval is 51%
		probability = predictionData["value"]
		if probability > 0.5:
			numbers.append(probability)
	if numbers.length > 0:
		return True
	else:
		return False

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
	app.run(debug=True)