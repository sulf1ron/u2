#!/usr/bin python3
# -*- coding:utf-8 -*-

import requests
import time
import configparser
import eventlet

cookies = dict(PHPSESSID='secret', nexusphp_u2='secret')
eventlet.monkey_patch()

while 1:
	url = 'https://u2.dmhy.org/'
	try:
		with eventlet.Timeout(3):
			t1 = time.time()
			page = requests.get(url = url, cookies = cookies)
			t2 = time.time()
		if (page.status_code == 200) & (not ('Server Error Encountered' in page.text)):
			status = 'online'
			delay = str(round(t2 - t1, 2))
		else:
			status = 'offline'
	except:
		status = 'offline'
	now = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
	if 'delay' not in locals().keys():
		delay = 'N/A'
	if 'page' in locals().keys():
		code = str(page.status_code)
	else:
		code = 'N/A'
	
	conf = configparser.ConfigParser()
	conf.add_section('U2')
	conf.set('U2', 'time', now)
	conf.set('U2', 'status', status)
	conf.set('U2', 'delay', delay)
	conf.set('U2', 'code', code)
	
	f = open('status.ini', 'w')
	conf.write(f)
	f.close()
	
	print('%s: %s, %s (%s)' % (now, status, delay, code))
	time.sleep(15)