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

def sql_select(name, table, column, value):
	sql = 'select %s from %s where %s = %s' % (name, table, column, value)
	execute(sql)
	return cursor.fetchone()[0]

def sql_update(table, column, value, ec, ev):
	sql = 'update %s set %s = %s where %s = %s' % (table, column, '%s', ec, ev)
	execute(sql, value)
	db.commit()
	return

def init(id, uid):
	captcha = random.randint(1000, 9999)
	sql = 'insert into user values (%s, %s, \'\', \'init\', -1, 0, 1, %s, %s, %s) on duplicate key update uid = %s, confirmed = 0, captcha = %s'
	execute(sql, id, uid, captcha, int(time.time()), 0, id, captcha)
	db.commit()
	return captcha

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
	sql = 'update `user` set mod_status = %s where id = %s'
	execute(sql, status, id)
	db.commit()
	return

def select_sm_status(id):
	sql = 'select sm_status from `user` where id = %s'
	execute(sql, id)
	status = cursor.fetchone()[0]
	return status

def select_sm_num(id):
	sql = 'select sm_num from `user` where id = %s'
	execute(sql, id)
	status = cursor.fetchone()[0]
	return status

def update_sm_status(id, status):
	sql = 'update `user` set sm_status = %s where id = %s'
	execute(sql, status, id)
	db.commit()
	return

def update_sm_num(id, num):
	sql = 'update `user` set sm_num = %s where id = %s'
	execute(sql, status, num)
	db.commit()
	return

def sm_num():
	sql = 'select * from sm order by id'
	return execute(sql)
	
def sm_init(uid):
	num = sm_num()
	sql = 'insert into sm (id, creator, disabled) values (%s, %s, 1)'
	execute(sql, num, uid)
	db.commit()
	return num
