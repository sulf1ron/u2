#!/usr/bin python3
# -*- coding:utf-8 -*-

'''
Author: Sulf1ron
Email: i@aalyp.cc
UID: 44929
'''

import pymysql
import configparser
import random
import time
import re

conf = configparser.ConfigParser()
conf.read('secret.ini')
dbconf = dict(conf.items('DB'))
db = pymysql.connect(dbconf['host'], dbconf['username'], dbconf['password'], dbconf['database'], charset = 'utf8')
cursor = db.cursor()

sql_log = open('sql.log', 'a')

def execute(sql):
	cursor.execute(sql)
	slog = '(%s) %s' % (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()), sql)
	print(slog)
	sql_log.write(slog + '\n')
	sql_log.flush()
	return

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
	sql = 'select * from sm order by id'
	cursor.execute(sql)
	mist = cursor.fetchall()
	pri = float('inf')
	for i in range(len(mist)):
		row = mist[i]
		if row[9]:
			continue
		match = re.match(row[4], text)
		if match is not None:
			if (row[3] < pri) & ( (row[5] and mod) or (random.random() < row[6]) ):
				pri = row[3]
				id = i
	if 'id' not in locals():
		return -1
	row = mist[id]
	if row[5] == 0:
		return row[7]
	else:
		if mod:
			return row[8]
		else:
			return row[7]

def mod_status(id):
	sql = 'select mod_status from `user` where id = %s' % (id)
	execute(sql)
	status = cursor.fetchone()[0]
	return status

def update_mod_status(id, status):
	sql = 'update `user` set mod_status = \'%s\' where id = %d' % (status, id)
	execute(sql)
	return