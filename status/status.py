#!/usr/bin python3
# -*- coding:utf-8 -*-

from flask import Flask, request, Response, render_template
from flask_mobility import Mobility
import configparser
import random
import json
import requests

app = Flask(__name__)
Mobility(app)

@app.route("/status.json")
def status_json():
	f = open('/var/www/status/status.json')
	data = json.load(f)
	f.close()
	del(data['rand'], data['title'], data['text'])
	return Response(json.dumps(data, ensure_ascii = False, indent = 4), mimetype = 'application/json')
	
@app.route("/")
def status():
	f = open('/var/www/status/status.json')
	data = json.load(f)
	f.close()

	if request.MOBILE:
		data['font'] = '125'
		data['width'] = '840'
		data['height'] = '750'
		return render_template('status.html', data = data)
	else:
		data['font'] = '62.5'
		data['width'] = '420'
		data['height'] = '375'
		return render_template('status.html', data = data)

if __name__ == "__main__":
#	t.start()
#	app.run(host = '0.0.0.0', port = 80)
	app.run(host = '0.0.0.0', port = 443, ssl_context = ('/etc/letsencrypt/live/status.dmhy.org/fullchain.pem', '/etc/letsencrypt/live/status.dmhy.org/privkey.pem'))