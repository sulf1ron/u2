#!/usr/bin python3
# -*- coding:utf-8 -*-

from locale import setlocale, atof
import requests
import re
import time
from bs4 import BeautifulSoup as bs

def cookie_verify():
	url = 'https://u2.dmhy.org'
	page = requests.get(url, cookies = cookies).text
	if 'U2分享園@動漫花園' in page:
		soup = bs(page, 'lxml')
		uid = soup.find_all('bdo', {'dir': 'ltr'})[0].parent.parent['href'][-5:]
		return uid
	else:
		return 0

def profile(uid):
	url = 'https://u2.dmhy.org/userdetails.php?id=' + uid
	page = requests.get(url, cookies = cookies).text
	soup = bs(page, 'lxml')
	try:
		data['avatar'] = soup.find('img', {'onload': "check_avatar(this, 'chs');"})['src']
	except:
		data['avatar'] = 'default.png'
	data['username'] = soup.find('bdo', {'dir': 'ltr'}).text
	try:
		data['uc-have'] = atof(soup.find('span', {'class': 'ucoin-notation'})['title'])
	except:
		data['uc-have'] = -1
	return data

from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def main():
	return render_template('index.html', data = data)

@app.route('/verify', methods = ['POST'])
def verify():
	if request.method == 'POST':
		global data, cookies
		cookies = {'nexusphp_u2': request.form['nexusphp_u2']}
		uid = cookie_verify()
		if not uid:
			return "-1"
		else:
			data['verfied'] = 1
			data = {**data, **profile(uid)}
			return "0"

@app.route('/set', methods = ['POST'])
def set():
	if request.method == 'POST':
		global data
		data['uc-sent'] = request.form['uc_sent']
		data['message'] = request.form['message']
		return "0"

data = {}
data['verfied'] = 0
data['username'] = '未登录'
data['avatar'] = 'static/default.png'
data['setted'] = 0

if __name__ == "__main__":
	import webbrowser
	webbrowser.open('http://localhost:2333')
	app.run(host = '0.0.0.0', port = 2333)