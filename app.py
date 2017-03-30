#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os
import urllib

from flask import Flask
from flask import request
from flask import make_response

userLocation = ""


keys= "&key=AIzaSyCUhQ42iZYv0A0ZVXdB0fLMga4Kj6lcyxU"
# Flask app should start in global layout
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
	req = request.get_json(silent=True, force=True)
    	print("Request:")
    	print(json.dumps(req, indent=4))
        res = processRequest(req)
        res = json.dumps(res, indent=4)
    # print(res)
        r = make_response(res)
        r.headers['Content-Type'] = 'application/json'
        return r

def processRequest(req):
	global userLocation
	if req.get("result").get("action") == "getUserLocation":
		result = req.get("result")
	    	parameters = result.get("parameters")
	    	location = parameters.get("areaname")
		if location=="":
			return {"speech": "enter your locality",
        			"displayText": "enter your locality",
        			"source": "apiai-weather-webhook-sample"}
		userLocation = location
        	res = makeWebhookResult()
		return res
	elif req.get("result").get("action") == "getBMI":
		result = req.get("result")
	    	parameters = result.get("parameters")
	    	heightInCm = parameters.get("height")
		weight=parameters.get("weight")
		height = float(float(heightInCm)/100)
		bmi = float(float(weight) / float(height*height))
		if (bmi>=18.5 and bmi<=25.0):
			return {"speech": "congrats! you are healthy",
        			"displayText": "congrats! you are healthy",
        			"source": "apiai-weather-webhook-sample"}
		elif(bmi>25.0 and bmi<=30.0):
			return {"speech": "um! its good if you loose some weight",
        			"displayText": "um! its good if you loose some weight",
        			"source": "apiai-weather-webhook-sample"}
		elif(bmi>30.0):
			return {"speech": "too much weight ! soo bad",
        			"displayText": "too much weight ! soo bad",
        			"source": "apiai-weather-webhook-sample"}
		else:
			return {"speech": "underweight!",
        			"displayText": "underweight!",
        			"source": "apiai-weather-webhook-sample"}
		


def makeWebhookResult():
	global userLocation
        speechz = ""
    	# print(json.dumps(item, indent=4))

    	URL2 = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=pharmacies%20in%20"+userLocation+"&key=AIzaSyBa1S1nslOslJn0je4OcVJ38YmBYs51KkY"
    	googleResponse = urllib.urlopen(URL2)
    	jsonResponse = json.loads(googleResponse.read())
    	#pprint.pprint(jsonResponse)
    	#test = json.dumps([s['name'] for s in jsonResponse['results']], indent=4)
    	response = []
    	for i in jsonResponse['results']:
			try:
				phoneUrl = "https://maps.googleapis.com/maps/api/place/details/json?placeid="
				resp = {}
				placeId = i['place_id']
				Url1 = phoneUrl+str(placeId)+keys
				phoneRes = urllib.urlopen(Url1)
				phoneResponse = json.loads(phoneRes.read())
				resp['phone'] = phoneResponse['result']['formatted_phone_number']
				resp['name'] = i['name']
				resp['address'] = i['formatted_address']
				response.append(resp)
			except KeyError:
				resp['phone'] = "Not Provided"
				resp['name'] = i['name']
				resp['address'] = i['formatted_address']
				response.append(resp)
				continue

    	stringBody=" "
    	for item in response:
        	stringBody = stringBody + "\n\n"
        	stringBody = stringBody+"name: "+item['name']+"\n"+"address: "+item['address']+"\n"+"phone: "+item['phone']

    	speechz = speechz + str(stringBody)

    	print("Response:")
    	print(speechz)

    	return {
        	"speech": speechz,
        	"displayText": speechz,
        # "data": data,
        # "contextOut": [],
        	"source": "apiai-weather-webhook-sample"
   	 }


if __name__ == '__main__':

    	port = int(os.getenv('PORT', 5000))

    	print("Starting app on port %d" % port)

    	app.run(debug=False, port=port, host='0.0.0.0')
