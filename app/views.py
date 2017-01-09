from flask import Flask, request
from flask_pymongo import PyMongo
from twilio import twiml
from clarifai import rest
from clarifai.rest import ClarifaiApp, Image as ClImage


app = Flask (__name__)
app.config['MONGO_DBNAME'] = 'photohunt'
app.config['MONGO_URI'] = 'mongodb://merp:derp@ds149258.mlab.com:49258/photohunt'
mongo = PyMongo(app)

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
	#fix this later	
	#elif str(request.form['ContentType'])!='image/jpeg':
	#	resp.message('Pictures only please!')
	#	return str(resp)

	elif photoGoals < 1:
		resp.message('Sure that\'s the right label?')
		return str(resp)
	else:
		url = request.form['MediaUrl0']
		resp.message(str(url))
		return str(resp)
		#return checkPhoto(request.form['MediaUrl'])

def checkPhoto(pictureURL, tag):
	resp = twiml.Response()
	photoApp = ClarifaiApp()
	model = photoApp.models.get(tag)
	#image = ClImage()
	resp.message(str(pictureURL))
	return str(resp)






if __name__ == '__main__':
	app.run(debug=True)