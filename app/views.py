from flask import Flask, request
from twilio import twiml

app = Flask (__name__)

@app.route('/sms', methods = ['POST'])
def sms():
	resp = twiml.Response()
	resp.message('#sophiescolon')
	return str(resp)

if __name__ == '__main__':
	app.run()