#!/usr/bin/python3
# -*- coding:utf-8 -*-

import requests
import time
import configparser
import eventlet
import json

conf = configparser.ConfigParser()
conf.read('secret.ini')
cookies = dict([('nexusphp_u2', conf.get('U2', 'nexusphp_u2'))])
eventlet.monkey_patch()

data = {}
url = 'https://u2.dmhy.org/'

try:
	with eventlet.Timeout(3):
		t1 = time.time()
		page = requests.get(url = url, cookies = cookies)
		t2 = time.time()
	if (page.status_code == 200) & (not ('Server Error Encountered' in page.text)):
		data['online'] = 1
		data['delay'] = str(round(t2 - t1, 2))
		data['code'] = 200
	else:
		data['online'] = 0
except:
	data['online'] = 0

data['time'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
if 'delay' not in data.keys():
	data['delay'] = -1
if 'page' in locals().keys():
	data['code'] = page.status_code
else:
	data['code'] = -1

with open('/var/www/status/status.json', 'w') as f:
	json.dump(data, f)
	f.close()

if __name__ == '__main__':
	print(json.dumps(data))