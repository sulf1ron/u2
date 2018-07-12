#!/usr/bin python3
# -*- coding:utf-8 -*-

import requests
import json
import time
import random

clothes = ['Animal', 'Kids', 'Winter', 'Witch']
host = ['hk', 'sh', 'jp', 'lon']

data = {}
data['now'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
data['delay'] = {}
count = 0
for loc in host:
	url = 'https://%s.sor.moe/status.json' % (loc)
	exec('%s = json.loads(requests.get(url).text)' % (loc))
	if eval('%s[\'online\']' % (loc)):
		data['delay'][loc] = eval('%s[\'delay\']' % (loc))
	else:
		count += 1
		data['delay'][loc] = -1

if count == 0:
	data['title'] = 'U2娘在线的呢'
	data['text'] = '不要老是盯着人家看啦w'
	f = open('/var/www/status/static/online.json')
else:
	data['title'] = 'U2娘开小差了'
	data['text'] = '你催人家也没有用的啦w'
	f = open('/var/www/status/static/offline.json')

live = json.load(f)
f.close()
live['textures'] = ['textures/%s.png' % (random.choice(clothes))]
f = open('/var/www/status/static/model.json', 'w')
json.dump(live, f)
f.close()

data['rand'] = str(random.randint(10, 99))

f = open('/var/www/status/status.json', 'w')
json.dump(data, f)
f.close()