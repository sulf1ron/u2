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

def execute(sql, *s):
	if s == ():
		slog = '(%s, sql) %s' % (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()), sql)
	else:
		slog = '(%s, sql) %s, %s' % (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()), sql, str(s))
	print(slog)
	sql_log.write(slog + '\n')
	sql_log.flush()
	return cursor.execute(sql, s)

def dbexit(sig, frame):
	db.close()
	print('bye~')
	exit()

def id2uid(id):
	sql = 'select uid from user where id = %s'
	if execute(sql, id) == 0:
		return -1 # 未绑定UID
	uid = cursor.fetchone()[0]
	return uid

def init(id, uid):
	captcha = random.randint(1000, 9999)
	sql = 'insert into user values (%s, %s, \'\', \'init\', 0, 1, %s) on duplicate key update uid = %s, confirmed = 0, captcha = %s'
	execute(sql, id, uid, captcha, uid, captcha)
	db.commit()
	return captcha
def select_captcha(id):
	sql = 'select captcha from user where id = %s'
	execute(sql, id)
	captcha = str(cursor.fetchone()[0])
	return captcha

def update_confirmed(id):
	sql = 'update user set confirmed = 1 where id = %s'
	execute(sql, id)
	db.commit()
	return

def update_captcha(id):
	captcha = random.randint(1000, 9999)
	sql = 'update user set captcha = %s where id = %s'
	execute(sql, captcha, id)
	db.commit()
	return captcha

def confirmed(id):
	sql = 'select confirmed from user where id = %s'
	execute(sql, id)
	confirmed = cursor.fetchone()[0]
	return confirmed

def newbie(uid):
	sql = 'select newbie from user where uid = %s'
	execute(sql, uid)
	newbie = cursor.fetchone()[0]
	return newbie

def old(uid):
	sql = 'update user set newbie = 0 where uid = %s'
	execute(sql, uid)
	db.commit()
	return

def sm(text, mod):
	sql = 'select * from sm order by id'
	execute(sql)
	mist = cursor.fetchall()
	pri = float('inf')
	for i in range(len(mist)):
		row = mist[i]
		if row[9]:
			continue
		match = re.search(row[4], text)
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
	sql = 'select mod_status from `user` where id = %s'
	execute(sql, id)
	status = cursor.fetchone()[0]
	return status

def update_mod_status(id, status):
	sql = 'update `user` set mod_status = \'%s\' where id = %s'
	execute(sql, status, id)
	db.commit()
	return