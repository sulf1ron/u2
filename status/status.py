#!/usr/bin python3
# -*- coding:utf-8 -*-

global online
global now

import requests
import time

cookies = dict(PHPSESSID='secret', nexusphp_u2='secret')

def judge():
	global online
	global now
	while 1:
		shoutbox = 'https://u2.dmhy.org/shoutbox.php?action=fetch&key=secret'
		u2 = 'https://u2.dmhy.org/'
		try:
			page = requests.get(url = u2, cookies = cookies, timeout = 3)
			page = requests.get(url = shoutbox, cookies = cookies, timeout = 3)
		except:
			online = 0
		finally:
			online = 1
		now = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
		time.sleep(30)
	return

from threading import Thread

t = Thread(target = judge)

from flask import Flask, request, render_template
from flask_mobility import Mobility

app = Flask(__name__)
Mobility(app)

@app.route("/")
def status():
	if request.MOBILE:
		if online:
			return render_template('1m.html', time = now)
		else:
			return render_template('2m.html', time = now)
	else:
		if online:
			return render_template('1d.html', time = now)
		else:
			return render_template('2d.html', time = now)

if __name__ == "__main__":
	t.start()
	app.run(host = '0.0.0.0', port = 443, ssl_context = ('fullchain.pem', 'privkey.pem'))