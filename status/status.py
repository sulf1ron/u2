#!/usr/bin python3
# -*- coding:utf-8 -*-

from flask import Flask, request, render_template
from flask_mobility import Mobility
import configparser
import random
import json

app = Flask(__name__)
Mobility(app)

clothes = ['Animal', 'Kids', 'Winter', 'Witch']

@app.route("/")
def status():
	data = {}
	conf = configparser.ConfigParser()
	conf.read('/var/www/status/status.ini')
	if conf.get('U2', 'status') == 'online':
		online = 1
		data['title'] = 'U2娘在线的呢'
		data['text'] = '不要老是盯着人家看啦w'
		f = open('/var/www/status/static/online.json')
	else:
		online = 0
		data['title'] = 'U2娘开小差了'
		data['text'] = '你催人家也没有用的啦w'
		f = open('/var/www/status/static/offline.json')
	live = json.load(f)
	f.close()
	live['textures'] = ['textures/%s.png' % (random.choice(clothes))]
	f = open('/var/www/status/static/model.json', 'w')
	json.dump(live, f)
	f.close()

	data['now'] = conf.get('U2', 'time')
	data['delay'] = conf.get('U2', 'delay')
	data['code'] = conf.get('U2', 'code')
	data['rand'] = str(random.randint(10, 99))
	
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
	app.run(host = '0.0.0.0', port = 80)
#	app.run(host = '0.0.0.0', port = 443, ssl_context = ('/etc/letsencrypt/live/status.dmhy.org/fullchain.pem', '/etc/letsencrypt/live/status.dmhy.org/privkey.pem'))