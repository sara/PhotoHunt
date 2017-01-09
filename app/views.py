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
	if userNums != 1:
		resp.message('Uh oh. Looks like this phone isn\'t part of the game!')
		return str(resp)
	if request.form['NumMedia'] != 1 or request.form['MediaContentType0']!='image/jpeg':
		resp.message('Make sure you attached one image')
		resp.message(str(rawUserNums))
		return str(resp)
	elif request.form['Body'].lower not in photoGoals:
		resp.message('Sure that\'s the right label?')
		return str(resp)
	else:
		resp = ('checkPhoto')
		return str(resp)
		#return checkPhoto(request.form['MediaUrl'])

#def checkPhoto(picture, tag):
	#photoApp = ClarifaiApp()
	#model = photoApp.models.get(tag)
	#image = ClImage()





if __name__ == '__main__':
	app.run(debug=True)