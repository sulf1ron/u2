# -*- coding:utf-8 -*-

'''
Author: 索尔@U2
Email: i@aalyp.cc
user: 44929
'''

from api import *

import re
from collections import Counter

from time import sleep
import time
import datetime

print('---参数设定---')
uc = int(input('赠送UC量: '))
good = input('发给好人的信息: ')
bad = input('发给坏人的信息: ')
print('---参数设定完毕---')

pattern = re.compile('\d+')
chain = input('请输入发糖串: \n')
user = pattern.findall(chain)

start = datetime.datetime.now()
print('---发糖脚本开始---')
current = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
print('开始时间: %s' % (current))

user = [int(x) for x in user]
cheater = Counter(user)
cheater.subtract(set(user))
cheater = set(list(cheater.elements())) # 重复发UID骗糖的坏人x
user = set(user) - cheater # 正常领糖的好人w

# 预处理 UID 合法性
print('---预处理UID---')
temp = set()
for uid in user:
	if valid(uid) == 0:
		temp.add(uid)
	else:
		print('不正确的UID: %s' % (uid))
user = temp
temp = set()
for uid in cheater:
	if valid(uid) == 0:
		temp.add(uid)
	else:
		print('不正确的UID: %s' % (uid))
cheater = temp
estimate = (len(user) + len(cheater)) * uc * 1.5 # 消耗UC
print('---预处理完毕---')
print('共发送%s份糖, 其中好人%s名, 坏人%s名' % (str(len(user) + len(cheater)), str(len(user)), str(len(cheater))))
print('预计消耗UC: %s' % (estimate))

print('---发糖进程开始---')
print('预热: 5分钟')
sleep(300)
total = 0

all = len(user) # 
min = all * 5
hrs = int(min / 60)
if hrs == 0:
	print('正在处理好人组(%s), 预计耗时: %s分钟' % (str(all), str(min)))
else:
	print('正在处理好人组(%s), 预计耗时: %s小时%s分钟' % (str(all), str(hrs), str(min)))
count = 1
for uid in user:
	retry = 1
	while online() == -1:
		retry += 1
		total += 1
		current = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
		print('(%s) U2娘抽风, 等待 5min 后重试... (尝试: %s)' % (current, str(retry)))
		sleep(300)
	#transfer(uid, uc, good)
	current = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
	print('(%s) %s/%s: %s' % (current, str(count), str(all), str(uid)))
	count += 1
	sleep(300)

all = len(cheater) # 
min = all * 5
hrs = int(min / 60)
if hrs == 0:
	print('正在处理坏人组(%s), 预计耗时: %s分钟' % (str(all), str(min)))
else:
	print('正在处理坏人组(%s), 预计耗时: %s小时%s分钟' % (str(all), str(hrs), str(min)))
count = 1
for uid in cheater:
	retry = 1
	while online() == -1:
		retry += 1
		total += 1
		current = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
		print('(%s) U2娘抽风, 等待 5min 后重试... (尝试: %s)' % (current, str(retry)))
		sleep(300)
	#transfer(uid, uc, good)
	current = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
	print( '(%s) %s/%s: %s' % (current, str(count), str(all), str(uid)) )
	count += 1
	sleep(300)

end = datetime.datetime.now()
print('---发糖进程结束---')
current = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
print('结束时间: %s' % (current))

delta = end - start
delta_gmtime = time.gmtime(delta.total_seconds())
duration = time.strftime("%H:%M:%S", delta_gmtime)
print('总耗时: %s, 其中U2娘掉线%s次' % (duration, str(total)))
print('---发糖脚本结束---')