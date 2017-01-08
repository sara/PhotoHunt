from flask import Flask, request
from flask_pymongo import PyMongo
from twilio import twiml

app = Flask (__name__)
app.config['MONGO_DBNAME'] = 'photohunt'
app.config['MONGO_URI'] = 'mongodb://merp:derp@ds149258.mlab.com:49258/photohunt'
mongo = PyMongo(app)

@app.route('/sms', methods = ['POST'])
def validate():
	resp = twiml.Response()

	#get teh list of valid user phone numbers and convert to usable array
	userNums = [str(x) for x in mongo.db.users.find()["phoneNumber"]]
	if request.form['From'] not in userNums:
		resp.message('Uh oh. Looks like this phone isn\'t part of the game!')
		return str(resp)
	elif request.form['NumMedia'] != 1 or request.form['MediaContentType0']!='image/jpeg':
		resp.message('Whoops! Check that you have 1 picture atteched')
		return str(resp)
	else:
		return checkPhoto(request.form['MediaUrl'])

def checkPhoto(picture)


if __name__ == '__main__':
	app.run()