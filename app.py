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
    res = makeWebhookResult()
    return res

def makeWebhookResult():
        speechz = "" 
        # print(json.dumps(item, indent=4))
        URL2 = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=pharmacies%20in%20thudialur&key=AIzaSyCYNf8FttdjFy8_SQORxX6ska6Xji4xEe0&format=json"     googleResponse = urllib.urlopen(URL2)
        jsonResponse = json.loads(googleResponse.read())
        #pprint.pprint(jsonResponse)
        #test = json.dumps([s['name'] for s in jsonResponse['results']], indent=4)
        for i in jsonResponse['results']:
            test=json.dumps(i['name']),json.dumps(i['formatted_address'])
            speechz = speechz + str(test) + '\n\n'

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
