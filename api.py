#!/usr/bin python3
# -*- coding:utf-8 -*-

'''
作者: 索尔
邮箱: i@aalyp.cc
UID:  44929
'''

from locale import *
import requests
import re
import time
from bs4 import BeautifulSoup as bs
import datetime
import json

# 设置数字格式
#setlocale(LC_NUMERIC, 'en_US.UTF-8')
setlocale(LC_NUMERIC, 'English_US')

# 通行证
my = 44929
cookies = dict(PHPSESSID='secret', nexusphp_u2='secret')

def myuid():
	return my

def online():
	url = 'https://u2.dmhy.org'
	try:
		page = requests.get(url, cookies = cookies, timeout = 3)
	except:
		return 0
	finally:
		return 1

def profile(uid):
	data = {}
	
	if type(uid) != int:
		data['code'] = 1 # uid 格式错误
		return data

	if not online():
		data['code'] = -1 # U2 离线
		return data
		
	url = 'https://u2.dmhy.org/userdetails.php?id=' + str(uid)
	page = requests.get(url, cookies = cookies).text
	soup = bs(page, 'lxml')
	if ('无效的ID' in page) or ('没有该ID的用户' in page):
		data['code'] = 2 # uid 不存在
		return data
		
	data['id'] = soup.find_all('bdo', {'dir': 'ltr'})[1].text
	if '用户想要保护其隐私' in page:
		data['code'] = 3 # 隐私强
		data['last'] = datetime.datetime.strptime(soup.find('time').text, '%Y-%m-%d %H:%M:%S')
		try:
			data['avatar'] = soup.find('img', {'onload': "check_avatar(this, 'chs');"})['src']
		except:
			data['avatar'] = 'https://u2.dmhy.org/pic/default_avatar.png'
		if data['avatar'][0:13] == '//u2.dmhy.org':
			data['avatar'] = 'https:' + data['avatar']
		return data
	
	data['code'] = 0 # 正常
	data['join'] = datetime.datetime.strptime(soup.find_all('time')[0].text, '%Y-%m-%d %H:%M:%S')
	data['last'] = datetime.datetime.strptime(soup.find_all('time')[2].text, '%Y-%m-%d %H:%M:%S')
# transfer
	data['transfer'] = {}
	try:
		data['transfer']['ratio'] = atof(soup.find(text='分享率').parent.parent.find('font').text)
	except:
		data['transfer']['ratio'] = 'inf'
	data['transfer']['upload'] = (atof(re.search('\d+(.\d+)?', soup.find(text='上传量').parent.parent.text).group()), soup.find(text='上传量').parent.parent.text[-3])
	data['transfer']['download'] = (atof(re.search('\d+(.\d+)?', soup.find(text='下载量').parent.parent.text).group()), soup.find(text='下载量').parent.parent.text[-3])
	data['transfer']['raw'] = {}
	data['transfer']['raw']['upload'] = (atof(re.search('\d+(.\d+)?', soup.find(text='实际上传').parent.parent.text).group()), soup.find(text='实际上传').parent.parent.text[-3])
	data['transfer']['raw']['download'] = (atof(re.search('\d+(.\d+)?', soup.find(text='实际下载').parent.parent.text).group()), soup.find(text='实际下载').parent.parent.text[-3])
# BT time
	data['time'] = {}
	data['time']['ratio'] = atof(soup.find(text='做种/下载时间比率').parent.parent.find('font').text)
	data['time']['seeding'] = atof(re.search('\d+', soup.find(text='做种时间').parent.parent.text).group())
	data['time']['leeching'] = atof(re.search('\d+', soup.find(text='下载时间').parent.parent.text).group())
# Network Bandwidth
	try:
		data['speed'] = {}
		data['speed']['download'] = (atof(soup.find('img', {'title': re.compile('下载:')})['title'][4:-4]), soup.find('img', {'title': re.compile('下载:')})['title'][-4].upper())
		data['speed']['upload'] = (atof(soup.find('img', {'title': re.compile('上传:')})['title'][4:-4]), soup.find('img', {'title': re.compile('上传:')})['title'][-4].upper())
	except:
		data['speed'] = 'N/A'
# Gender
	data['gender'] = soup.find(text='性别').parent.next_sibling.img['title']
# Avatar
	try:
		data['avatar'] = soup.find('img', {'onload': "check_avatar(this, 'chs');"})['src']
	except:
		data['avatar'] = 'https://u2.dmhy.org/pic/default_avatar.png'
	if data['avatar'][0:13] == '//u2.dmhy.org':
		data['avatar'] = 'https:' + data['avatar']
# Class
	data['class'] = soup.find(text='等级').parent.next_sibling.img['title']
	try:
		data['title'] = soup.find(text='等级').parent.next_sibling.img.next_sibling.next_sibling.text
	except:
		data['title'] = 'N/A'
# Experience
	data['exp'] = int(re.search('\d+', soup.find(text=re.compile('EXP'))).group())
# UCoin
	data['uc'] = {}
	data['uc']['amount'] = atof(soup.find_all('span', {'class': 'ucoin-notation'})[1]['title'])
	data['uc']['gold'] = int(data['uc']['amount'] // 10000)
	data['uc']['silver'] = int((data['uc']['amount'] - data['uc']['gold'] * 10000) // 100)
	data['uc']['copper'] = int(data['uc']['amount'] % 100)
	return data
	
def valid(uid):
	data = profile(uid)
	err = data['code']
	if err == -1:
		return -1 # 离线
	elif (err == 0) or (err == 3):
		return 1 # 有效
	else:
		return 0 # 无效
		
def id(uid):
	data = profile(uid)
	err = data['code']
	if err == -1:
		return -1 # 离线
	elif (err == 0) or (err == 3):
		return data['id'] # 有效
	else:
		return 1 # 无效

def uc(uid):
	data = profile(uid)
	err = data['code']
	if err == -1:
		return -1 # 离线
	elif err == 3:
		return 2 # 隐私强
	elif err == 0:
		return data['uc']['amount']
	else:
		return 1 # 不存在

def pm(uid, subject, body, save):
	if not online():
		return -1 # 离线
	if not valid(uid):
		return 1 # uid 不存在
	url = 'https://u2.dmhy.org/takemessage.php'
	data = {}
	data['receiver'] = str(uid)
	data['returnto'] = 'https://u2.dmhy.org/messages.php?action=viewmailbox&box=-1'
	data['subject'] = subject
	data['body'] = body
	data['save'] = save
	page = requests.post(url = url, cookies = cookies, data = data).text
	return 0
	
def speed(uid):
	data = {}
	if not online():
		data['code'] = -1 # -1: 离线
		return data
		
	elif not valid(uid):
		data['code'] = 1 # uid 不存在
		return data
	data['code'] = 0
	url = 'https://u2.dmhy.org/httpapi_ucoinspeed.php?type=d&uid=' + str(uid)
	page = requests.get(url, cookies = cookies)
	recv = json.loads(page.text)
	if recv['amount'] > recv['interval']:
		data['type'] = 0 # 秒壕
		data['speed'] = round(recv['amount'] / recv['interval'], 3)
	else:
		data['type'] = 1 # 穷逼
		data['speed'] = round(recv['amount'] / (recv['interval'] / 3600), 3)
	return data
	
def salary(uid, type):
	data = {}
	if not online():
		data['code'] = -1 # -1: 离线
		return data
	elif not valid(uid):
		data['code'] = 1 # uid 不存在
		return data
	data['code'] = 0
	url = 'https://u2.dmhy.org/httpapi_ucoinspeed.php?type=%s&uid=' % (type) + str(uid)
	page = requests.get(url, cookies = cookies)
	recv = json.loads(page.text)
	data['uc'] = recv['amount']
	return data
		
def magic(id, utime, ur, dr, target):
	if not online():
		return -1
	url = 'https://u2.dmhy.org/promotion.php?action=magic&torrent=' + str(id)
	page = requests.get(url, cookies = cookies).text
	soup = bs(page, 'lxml')
	data = {}
	data['action'] = soup.find('input', {'name': 'action'})['value']
	data['divergence'] = soup.find('input', {'name': 'divergence'})['value']
	data['base_everyone'] = soup.find('input', {'name': 'base_everyone'})['value']
	data['base_self'] = soup.find('input', {'name': 'base_self'})['value']
	data['base_other'] = soup.find('input', {'name': 'base_other'})['value']
	data['torrent'] = soup.find('input', {'name': 'torrent'})['value']
	data['tsize'] = soup.find('input', {'name': 'tsize'})['value']
	data['ttl'] = soup.find('input', {'name': 'ttl'})['value']
	if type(target) == int:
		data['user'] = 'OTHER'
		data['user_other'] = target
	else:
		data['user'] = target.upper()
	data['start'] = 0
	data['hours'] = utime
	data['promotion'] = 8
	data['ur'] = ur
	data['dr'] = dr
	data['comment'] = 'u2bot@tg'
	url = 'https://u2.dmhy.org/promotion.php?test=1'
	page = requests.post(url, cookies = cookies, data = data).text
	soup = bs(page, 'lxml')
	ucost = atof(soup.find('span', {'class': '\\"ucoin-notation\\"'})['title'][2:-2])
	url = 'https://u2.dmhy.org/promotion.php?action=magic&torrent=' + str(id)
	page = requests.post(url, cookies = cookies, data = data)
	return str(ucost)
	
def transfer(uid, amount, message):
	data = {}
	if not online():
		return -1 # timeout
	elif not valid(uid):
		return 1 # uid 不存在
	data['event'] = '1003'
	data['recv'] = uid
	data['amount'] = amount
	data['message'] = message
	url = 'https://u2.dmhy.org/mpshop.php'
	page = requests.post(url, cookies = cookies, data = data).text
	if '请勿进行频繁转账' in page:
		return 2 # 冷却期
	else:
		return 0 # 成功

def get(url):
	try:
		data = requests.get(url, cookies = cookies, timeout = 3)
	except:
		return -1 # 离线
	finally:
		return data