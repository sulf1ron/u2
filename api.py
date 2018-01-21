# -*- coding:utf-8 -*-

'''
Author: 索尔@U2
Email: i@aalyp.cc
UID: 44929
'''

import re
import time
import requests
from bs4 import BeautifulSoup as bs
import datetime
from locale import *
import json

# 设置数字格式
setlocale(LC_NUMERIC, 'en_US.UTF-8')
#setlocale(LC_NUMERIC, 'English_US')

# Token
myuid = 44929 # uid
cookie = dict(PHPSESSID='secret', nexusphp_u2='secret')

# 获取个人信息
def profile(uid):
	data = {}
	if type(uid) != int:
		data['error'] = -2 # -2: uid格式不正确
		return data
	url = 'https://u2.dmhy.org/userdetails.php?id=' + str(uid)
	try:
		page = requests.get(url, cookies = cookie, timeout = 3).text
	except:
		data['error'] = -1 # -1: Time out
		return data
	soup = bs(page, 'lxml')
	if ('无效的ID' in page) or ('没有该ID的用户' in page):
		data['error'] = 1 # 1: uid不存在
		return data
	data['id'] = soup.find_all('bdo', {'dir': 'ltr'})[1].text
	if '用户想要保护其隐私' in page:
		data['error'] = 2 # 2: 用户隐私为强
#		data['last'] = datetime.datetime.strptime(soup.find('time').text, '%Y-%m-%d %H:%M:%S')
		data['last'] = soup.find('time').text
		try:
			data['avatar'] = soup.find('img', {'onload': "check_avatar(this, 'chs');"})['src']
		except:
			data['avatar'] = 'https://u2.dmhy.org/pic/default_avatar.png'
		if data['avatar'][0:13] == '//u2.dmhy.org':
			data['avatar'] = 'https:' + data['avatar']
		return data
	data['error'] = 0 # 0: 无错误
#	data['join'] = datetime.datetime.strptime(soup.find_all('time')[0].text, '%Y-%m-%d %H:%M:%S')
#	data['last'] = datetime.datetime.strptime(soup.find_all('time')[2].text, '%Y-%m-%d %H:%M:%S')
	data['join'] = soup.find_all('time')[0].text
	data['last'] = soup.find_all('time')[2].text
# transfer
	data['transfer'] = {}
	try:
		data['transfer']['ratio'] = soup.find(text='分享率').parent.parent.find('font').text
	except:
		data['transfer']['ratio'] = 'inf'
	data['transfer']['upload'] = (re.search('\d+(.\d+)?', soup.find(text='上传量').parent.parent.text).group(), soup.find(text='上传量').parent.parent.text[-3])
	data['transfer']['download'] = (re.search('\d+(.\d+)?', soup.find(text='下载量').parent.parent.text).group(), soup.find(text='下载量').parent.parent.text[-3])
	data['transfer']['raw'] = {}
	data['transfer']['raw']['upload'] = (re.search('\d+(.\d+)?', soup.find(text='实际上传').parent.parent.text).group(), soup.find(text='实际上传').parent.parent.text[-3])
	data['transfer']['raw']['download'] = (re.search('\d+(.\d+)?', soup.find(text='实际下载').parent.parent.text).group(), soup.find(text='实际下载').parent.parent.text[-3])
# BT time
	data['bt'] = {}
	data['bt']['ratio'] = soup.find(text='做种/下载时间比率').parent.parent.find('font').text
	data['bt']['seeding'] = re.search('\d+', soup.find(text='做种时间').parent.parent.text).group()
	data['bt']['leeching'] = re.search('\d+', soup.find(text='下载时间').parent.parent.text).group()
# Network Bandwidth
	try:
		data['speed'] = {}
		data['speed']['download'] = (soup.find('img', {'title': re.compile('下载:')})['title'][4:-4], soup.find('img', {'title': re.compile('下载:')})['title'][-4].upper())
		data['speed']['upload'] = (soup.find('img', {'title': re.compile('上传:')})['title'][4:-4], soup.find('img', {'title': re.compile('上传:')})['title'][-4].upper())
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
	data['exp'] = re.search('\d+', soup.find(text=re.compile('EXP'))).group()
# UCoin
	data['uc'] = {}
	data['uc']['amount'] = atof(soup.find_all('span', {'class': 'ucoin-notation'})[1]['title'])
	data['uc']['gold'] = int(data['uc']['amount'] // 10000)
	data['uc']['silver'] = int((data['uc']['amount'] - data['uc']['gold'] * 10000) // 100)
	data['uc']['copper'] = int(data['uc']['amount'] % 100)
	return data

def pm(uid, subject, body, save):
	url = 'https://u2.dmhy.org/takemessage.php'
	data = {}
	data['receiver'] = str(uid)
	data['returnto'] = 'https://u2.dmhy.org/messages.php?action=viewmailbox&box=-1'
	data['subject'] = subject
	data['body'] = body
	data['save'] = save
	page = requests.post(url, cookies = cookie, data = data).text
	return
	
def speed(uid):
	data = {}
	recv = profile(uid)
	if recv['error'] == -1:
		data['error'] = -1 # -1: timeout
		return data
	elif (recv['error'] != 0) and (recv['error'] != 2):
		data['error'] = 1
		return data
	url = 'https://u2.dmhy.org/httpapi_ucoinspeed.php?type=d&uid=' + str(uid)
	try:
		page = requests.get(url, cookies = cookie, timeout = 3)
	except:
		data['error'] = -1 # time out
		return(data)
	recv = json.loads(page.text)
	if recv['code'] == -1:
		data['error'] = 1 # uid不存在
		return data
	data['error'] = 0
	if recv['amount'] > recv['interval']:
		data['type'] = 0 # 秒壕
		data['speed'] = round(recv['amount'] / recv['interval'], 3)
	else:
		data['type'] = 1 # 穷逼
		data['speed'] = round(recv['amount'] / (recv['interval'] / 3600), 3)
	return data
	
def salary(uid, type):
	data = {}
	recv = profile(uid)
	if recv['error'] == -1:
		data['error'] = -1 # -1: timeout
		return data
	elif (recv['error'] != 0) and (recv['error'] != 2):
		data['error'] = 1
		return data
	url = 'https://u2.dmhy.org/httpapi_ucoinspeed.php?type=%s&uid=' % (type) + str(uid)
	try:
		page = requests.get(url, cookies = cookie, timeout = 3)
	except:
		data['error'] = -1 # time out
		return(data)
	recv = json.loads(page.text)
	data['error'] = 0
	data['uc'] = recv['amount']
	return data

def online():
	url = 'https://u2.dmhy.org'
	try:
		page = requests.get(url, cookies = cookie, timeout = 3)
		return 1
	except:
		return 0
		
def magic(id, utime, ur, dr, target):
	url = 'https://u2.dmhy.org/promotion.php?action=magic&torrent=' + str(id)
	page = requests.get(url, cookies = cookie).text
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
	page = requests.post(url, cookies = cookie, data = data).text
	soup = bs(page, 'lxml')
	ucost = atof(soup.find('span', {'class': '\\"ucoin-notation\\"'})['title'][2:-2])
	url = 'https://u2.dmhy.org/promotion.php?action=magic&torrent=' + str(id)
	page = requests.post(url, cookies = cookie, data = data)
	return str(ucost)
	
def transfer(uid, amount, message):
	data = {}
	data['event'] = '1003'
	data['recv'] = uid
	data['amount'] = amount
	data['message'] = message
	url = 'https://u2.dmhy.org/mpshop.php'
	page = requests.post(url, cookies = cookie, data = data).text
	if '请勿进行频繁转账' in page:
		return 0 # 成功
	else:
		return 1 # 失败