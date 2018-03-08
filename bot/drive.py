#!/usr/bin python3
# -*- coding:utf-8 -*-

'''
Author: Sulf1ron
Email: i@aalyp.cc
UID: 44929
'''

import pymysql
import configparser

conf = configparser.ConfigParser()
conf.read('secret.ini')
dbconf = dict(conf.items('DB'))
db = pymysql.connect(dbconf['host'], dbconf['username'], dbconf['password'], dbconf['database'], charset = 'utf8')
cursor = db.cursor()

def dbexit(sig, frame):
	db.close()
	print('bye~')
	exit()

def id2uid(id):
	sql = 'select uid from user where id = %s' % (id)
	if cursor.execute(sql) == 0:
		return -1 # 未绑定UID
	uid = cursor.fetchone()[0]
	return uid

def confirmed(id):
	sql = 'select confirmed from user where id = %s' % (id)
	cursor.execute(sql)
	confirmed = cursor.fetchone()[0]
	return confirmed

def newbie(uid):
	sql = 'select newbie from user where uid = %s' % (uid)
	cursor.execute(sql)
	newbie = cursor.fetchone()[0]
	return newbie

def old(uid):
	sql = 'update user set newbie = 0 where uid = %s' % (uid)
	cursor.execute(sql)
	return

def sm(text, mod):
	sql = 'select * from sm'
	cursor.execute(sql)
	mist = cursor.fetchall()
	pri = float('inf')
	for i in range(len(mist)):
		row = mist[i]
		if row[4] in text:
			if row[3] < pri:
				pri = row[3]
				id = i
	if 'id' not in locals():
		return -1
	row = mist[id]
	if row[5] == 0:
		return row[6]
	else:
		if mod:
			return row[7]
		else:
			return row[6]