#!/usr/bin python3
# -*- coding:utf-8 -*-

'''
Author: 索尔@U2
Email: i@aalyp.cc
UID: 44929
'''

from api import *

import logging
import sys

import re
from collections import Counter

from time import sleep
import time
import datetime

def isnum(s):
	try:
		num = float(s)
		return 1
	except:
		return 0

logger = logging.getLogger('sweet')
formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')
file_handler = logging.FileHandler('sweet.log')
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.formatter = formatter
logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.setLevel(logging.INFO)
#l = open('sweet.log', 'wb')

print('---参数设定---')
uctg = input('赠送好人 UCoin 量: ')
while not isnum(uctg):
	logger.error('格式不正确!')
	uctg = input('赠送好人 UCoin 量: ')
uctg = int(uctg)
uctb = input('赠送坏人 UCoin 量: ')
while not isnum(uctb):
	logger.error('格式不正确!')
	uctb = input('赠送坏人 UCoin 量: ')
uctb = int(uctb)
msgg = input('发给好人的信息: ')
msgb = input('发给坏人的信息: ')
print('---参数设定完毕---')

chain = input('请输入发糖串: \n')

print('---发糖脚本开始---')
start = datetime.datetime.now()
logger.info('进程启动')
total = 0 # 总尝试次数

pattern = re.compile('\d{5}|\d{3}')
bank = chain.split('<--')
bank = [re.sub('\[em\d+]', '', text) for text in bank] # 去除 emoji
g = []
for text in bank:
	uid = pattern.findall(text)
	if uid != []:
		g.append(int(uid[0]))

b = Counter(g)
b.subtract(set(g))
b = set(list(b.elements())) # 重复发UID骗糖的坏人x
g = set(g) - b # 正常领糖的好人w

str1 = '{' + ', '.join(str(uid) for uid in g) + '}'
str2 = '{' + ', '.join(str(uid) for uid in b) + '}'
logger.info('好人: \n                                  %s', str1)
logger.info('坏人: \n                                  %s', str2)
# 预处理 UID 合法性
print('---预处理UID---')
temp = set()
for uid in g:
	retry = 0
	status = valid(uid)
	while status == -1:
		retry += 1
		total += 1
		logger.error('U2娘抽风, 等待 5mins 后重试... (尝试: %d)', retry)
		sleep(300)
		status = valid(uid)
	if status:
		temp.add(uid)
	else:
		logger.warning('不正确的UID: %d', uid)
g = temp

temp = set()
for uid in b:
	retry = 0
	status = valid(uid)
	while status == -1:
		retry += 1
		total += 1
		logger.error('U2娘抽风, 等待 5mins 后重试... (尝试: %d)', retry)
		sleep(300)
		status = valid(uid)
	if status:
		temp.add(uid)
	else:
		logger.warning('不正确的UID: %d', uid)
b = temp

estimate = len(g) * (uctg * 1.5 + 100) + len(b) * (uctb * 1.5 + 100) # 消耗UC
print('---预处理完毕---')

str1 = '{' + ', '.join(str(uid) for uid in g) + '}'
str2 = '{' + ', '.join(str(uid) for uid in b) + '}'
logger.info('实发好人: \n                                  %s', str1)
logger.info('实发坏人: \n                                  %s', str2)

logger.info('共发送%d份糖, 其中好人%s名, 坏人%s名', len(g) + len(b), len(g), len(b))
logger.info('预计消耗UC: %.2f', estimate)

myuc = uc(myuid())
while myuc == -1:
	retry += 1
	total += 1
	logger.error('U2娘抽风, 等待 5mins 后重试... (尝试: %d)', retry)
	sleep(300)
	myuc = uc(myuid())
if myuc > 2:
	logger.info('当前UCoin存量: %.2f', myuc)
	if myuc < estimate:
		logger.critical('UCoin存量不足!')
		print('---发糖脚本结束---')
		exit()	
	else:
		print('---发糖进程开始---')

logger.info('预热: 5分钟')
sleep(300)

turn = 0
tm = max(uctg // 50000, uctb // 50000) + 1
tu = len(g) * (uctg // 50000 + 1) + len(b) * (uctb // 50000 + 1)
ttm = tu * 5
tth = ttm // 60
ttm -= tth * 60
logger.info('共发送%d份, 预计耗时: %d小时%d分钟', tu, tth, ttm)
des = datetime.datetime.now() + datetime.timedelta(hours = tth, minutes = ttm)
logger.info('预计完成时间: %s', des.strftime("%Y-%m-%d %H:%M:%S"))

num = 1
while (uctg > 0) or (uctb > 0):
	turn += 1
	ucg = min(uctg, 50000)
	ucb = min(uctb, 50000)
	uctg -= ucg
	uctb -= ucb
	print('---第 (%d/%d) 轮---' % (turn, tm))
	
	retry = 0
	if ucg > 0:
		all = len(g)
		mins = all * 5
		hrs = mins // 60
		mins -= hrs * 60
		if hrs == 0:
			logger.info('正在处理好人组(%d), 预计耗时: %d分钟', all, mins)
		else:
			logger.info('正在处理好人组(%d), 预计耗时: %d小时%d分钟', all, hrs, mins)
		count = 1
		for uid in g:
			status = transfer(uid, ucg, msgg)
			status = 0
			while status == -1:
				retry += 1
				total += 1
				logger.error('U2娘抽风, 等待 5mins 后重试... (尝试: %d)', retry)
				sleep(300)
				status = transfer(uid, ucg, msgg)
			if status == 0:
				logger.info('%d/%d (%d/%d): %d', count, all, num, tu, uid)
			else:
				logger.info('%d/%d (%d/%d): %d 未知错误', count, all, num, tu, uid)
			count += 1
			num += 1
			if not num == tu:
				sleep(300)

	if ucb > 0:
		all = len(b)
		mins = all * 5
		hrs = mins // 60
		if hrs == 0:
			logger.info('正在处理坏人组(%d), 预计耗时: %s分钟', all, mins)
		else:
			logger.info('正在处理坏人组(%d), 预计耗时: %d小时%d分钟', all, hrs, mins)
		count = 1
		for uid in b:
			retry = 0
			status = transfer(uid, ucb, msgb)
			while status == -1:
				retry += 1
				total += 1
				logger.error('U2娘抽风, 等待 5mins 后重试... (尝试: %d)', retry)
				sleep(300)
				status = transfer(uid, ucb, msgb)
			if status == 0:
				logger.info('%d/%d (%d/%d): %d', count, all, num, tu, uid)
			else:
				logger.info('%d/%d (%d/%d): %d 未知错误', count, all, num, tu, uid)
			count += 1
			num += 1
			if not num == tu:
				sleep(300)

	
end = datetime.datetime.now()
print('---发糖进程结束---')
current = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
logger.info('结束时间: %s' % (current))

delta = end - start
delta_gmtime = time.gmtime(delta.total_seconds())
duration = time.strftime("%H:%M:%S", delta_gmtime)
logger.info('总耗时: %s, 其中U2娘掉线%d次', duration, total)
print('---发糖脚本结束---')