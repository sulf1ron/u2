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

# 设置数字格式
setlocale(LC_NUMERIC, 'en_US.UTF-8')
#setlocale(LC_NUMERIC, 'English_US')

# Token
myuid = 44929 # uid
cookie = dict(PHPSESSID='secret', nexusphp_u2='secret')

# 获取个人信息
def u2_profile(uid):
	data = {}
	url = 'https://u2.dmhy.org/userdetails.php?id=' + uid
	page = requests.get(url, cookies = cookie).text
	soup = bs(page, 'lxml')
	if '没有该ID的用户' in page:
		data['error'] = '-1' # -1: 没有该ID的用户
		return data
	data['id'] = soup.find_all('bdo', {'dir': 'ltr'})[1].text
	if '用户想要保护其隐私' in page:
		data['error'] = '2' # 2: 用户隐私为强
#		data['last'] = datetime.datetime.strptime(soup.find('time').text, '%Y-%m-%d %H:%M:%S')
		data['last'] = soup.find('time').text
		return data
	data['error'] = '0' # 0: 无错误
#	data['join'] = datetime.datetime.strptime(soup.find_all('time')[0].text, '%Y-%m-%d %H:%M:%S')
#	data['last'] = datetime.datetime.strptime(soup.find_all('time')[2].text, '%Y-%m-%d %H:%M:%S')
	data['join'] = soup.find_all('time')[0].text
	data['last'] = soup.find_all('time')[2].text
# transfer
	data['transfer'] = {}
	data['transfer']['share ratio'] = soup.find(text='分享率').parent.parent.find('font').text
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
		data['speed']['download'] = soup.find('img', {'title': re.compile('下载:')})['title'][4:]
		data['speed']['upload'] = soup.find('img', {'title': re.compile('上传:')})['title'][4:]
	except:
		data['speed'] = 'N/A'
# Gender
	data['gender'] = soup.find(text='性别').parent.next_sibling.img['title']
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
	data['uc']['gold'] = soup.find_all('span', {'class': 'ucoin-symbol ucoin-gold'})[1].text
	data['uc']['silver'] = soup.find_all('span', {'class': 'ucoin-symbol ucoin-silver'})[1].text
	data['uc']['copper'] = soup.find_all('span', {'class': 'ucoin-symbol ucoin-copper'})[1].text
	return data
