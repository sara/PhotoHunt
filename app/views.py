from flask import Flask, request
from flask_pymongo import PyMongo
from twilio import twiml
from clarifai import rest
from clarifai.rest import ClarifaiApp, Image as ClImage


app = Flask (__name__)
app.config['MONGO_DBNAME'] = 'photohunt'
app.config['MONGO_URI'] = 'mongodb://merp:derp@ds149258.mlab.com:49258/photohunt'
mongo = PyMongo(app)
globalRank = 1;

@app.route('/sms', methods = ['POST'])
def validate():
	resp = twiml.Response()
	userNums = mongo.db.users.count({"phoneNumber": request.form['From']})
	photoGoals = mongo.db.photoGoals.count({"item":request.form['Body']})
	if userNums != 1:
		resp.message('Uh oh. Looks like this phone isn\'t part of the game!')
		return str(resp)
	elif int(request.form['NumMedia']) != 1:
		resp.message('Make sure you attach one picture')
		return str(resp)
	#verify this later	
	#elif str(request.form['MediaContentType0'])!='image/jpeg':
	#	resp.message('Pictures only please!')
	#	return str(resp)

	elif photoGoals < 1:
		resp.message('Sure that\'s the right label?')
		return str(resp)
	else:
		url = request.form['MediaUrl0']
		tag = request.form['Body']
		if (checkPhoto(url, tag)):
			updateProfile(userNums, tag)
			resp.message(updateProfile(request.form['From'], tag))
		else:
			resp.message('Sorry, that picture doesn\'t count')
		return str(resp)

def checkPhoto(pictureURL, tag):
	resp = twiml.Response()
	photoApp = ClarifaiApp()
	conceptGoals = [str(x) for x in mongo.db.photoGoals.find_one({"item":tag})["concepts"]]
	model = photoApp.models.get(tag)
	image = ClImage(url = pictureURL)
	predictionData = model.predict([image])["data"]
	conceptsPresent = conceptGoals.intersection(predictionData["name"])
	numbers = []
	for x in conceptsPresent:
		probability = predictionData["value"]
		if probability > 0.5:
			numbers.append(probability)
	if numbers.length > 2:
		return True
	else:
		return False

def updateProfile(phoneNumber, tag)
	mongo.db.users.update_one(
		{"phoneNumber":phoneNumber,
		 "item":tag},
		{
			$set: {"scoresheet.$.found":true},
			$inc: {"numFound": 1}
		})
	if mongo.db.users.find_one({"phoneNumber":phoneNumber})["numFound"] == 5:
		globalRank += 1
		return ('Good job, looks like you\'re done! You #' + globalRank-1 + ' to finish!')
	else:
		return ('Way to go! Your score has been adjusted')
		

if __name__ == '__main__':
	app.run(debug=True)