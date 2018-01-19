# -*- coding:utf-8 -*-

'''
Author: Sulf1ron
Email: i@aalyp.cc
'''
import signal
def exit():
	db.close()
	print('Bye~')
	exit()
signal.signal(signal.SIGINT, exit)
signal.signal(signal.SIGTERM, exit)

import telegram
bot = telegram.Bot(token='secret')
print(bot.getMe())

from telegram.ext import Updater
updater = Updater(token='secret')
dispatcher = updater.dispatcher

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def main(bot, update, chat_data, user_data):
	id = update.effective_user.id
	uid = id2uid(id)
	text = update.effective_message['text']
	if text[0:3] != '幼兔娘':
		return
	if uid == -1:
		bot.send_message(chat_id=update.message.chat_id, text='主人请先告诉幼兔娘UID~')
		return
	if not confirmed(id):
		bot.send_message(chat_id=update.message.chat_id, text='先去验明真身哼')
		return
	text = text[4:]
	if '赚分速度' in text:
		bot_speed(bot, update, uid)
		return
	if ('UC' in text) or ('uc' in text):
		bot_uc(bot, update, uid)
		return
	if ('看看我的头像') in text:
		bot_avatar(bot, update, uid)
		return
	bot.send_message(chat_id=update.message.chat_id, text=text)
from telegram.ext import MessageHandler, Filters
echo_handler = MessageHandler(Filters.text, main, pass_chat_data=True, pass_user_data=True)
dispatcher.add_handler(echo_handler)


from api import *

from telegram.ext import CommandHandler
updater.start_polling()

### set ###
import pymysql
import random
db = pymysql.connect('localhost', 'root', 'MySQI@102914', 'u2bot')
cursor = db.cursor()

def id2uid(id):
	sql = 'select uid from user where id = %s' % (id)
	if cursor.execute(sql) == 0:
		return -1
	uid = cursor.fetchone()[0]
	return uid

def confirmed(id):
	sql = 'select confirmed from user where id = %s' % (id)
	cursor.execute(sql)
	confirmed = cursor.fetchone()[0]
	return confirmed

def set(bot, update, args, user_data):
	id = update.effective_user['id']
	if (id2uid(id) != -1) and (confirmed(id)):
		bot.send_message(chat_id=update.message.chat_id, text='已经知道主人的身份啦，不用重复验证喵')
		return
	uid = ' '.join(args)
	data = profile(int(uid))
	if (data['error'] != 0) and (data['error'] != 2):
		bot.send_message(chat_id=update.message.chat_id, text='竟然敢欺骗本兔子，人家不理你了哼！')
		return
	captcha = str(random.randint(1000, 9999))
	sql = 'insert into user values (%s, %s, 0, 1, %s) on duplicate key update uid = %s, confirmed = 0, captcha = %s' % (id, uid, captcha, uid, captcha)
	cursor.execute(sql)
	db.commit()
	pm(int(uid), '验证码', captcha, 'yes')
	bot.send_message(chat_id=update.message.chat_id, text='验证码已经发送给主人了喵，快去查收w')
	return
set_handler = CommandHandler('set', set, pass_args=True, pass_user_data=True)
dispatcher.add_handler(set_handler)

### confirm ###
def confirm(bot, update, args, user_data):
	id = update.effective_user['id']
	if id2uid(id) == -1:
		bot.send_message(chat_id=update.message.chat_id, text='请先设置UID！')
		return
#	sql = 'select confirmed from user where id = %s' % (id)
#	cursor.execute(sql)
#	confirmed = cursor.fetchone()[0]
	if confirmed(id):
		bot.send_message(chat_id=update.message.chat_id, text='已验证过无需再次验证')
		return
	captcha = ' '.join(args)
	sql = 'select captcha from user where id = %s' % (id)
	cursor.execute(sql)
	real = str(cursor.fetchone()[0])
	if real == captcha:
		sql = 'update user set confirmed = 1 where id = %s' % (id)
		cursor.execute(sql)
		db.commit()
		bot.send_message(chat_id=update.message.chat_id, text='身份验证成功')
	else:
		captcha = str(random.randint(1000, 9999))
		sql = 'update user set captcha = %s where id = %s' % (captcha, id)
		cursor.execute(sql)
		db.commit()
		bot.send_message(chat_id=update.message.chat_id, text='验证不通过，请查收新生成的验证码')
	return
confirm_handler = CommandHandler('confirm', confirm, pass_args=True, pass_user_data=True)
dispatcher.add_handler(confirm_handler)

### UCoin ###
def bot_uc(bot, update, uid):
	data = profile(uid)
	if data['error'] == -1:
		word = ['无法与U2娘建立神经元连接QAQ']
	elif data['error'] == 0:
		if int(data['uc']['gold']) > 200:
			text = [data['id'] + '：' + str(data['uc']['gold']) + '金 ' + str(data['uc']['silver']) + '银 ' + str(data['uc']['copper']) + '铜', '哦哦哦好多小钱钱$_$，快拿来给我吃大餐！']
		else:
			text = [data['id'] + '：' + str(data['uc']['gold']) + '金 ' + str(data['uc']['silver']) + '银 ' + str(data['uc']['copper']) + '铜', '虽，虽然养不活幼兔娘不过没关系啦']
#	elif data['error'] == 1:
#		text = ['这只兔子失踪了QAQ']
	elif data['error'] == 2:
		text = [data['id'] + '你这只傲娇不给幼兔娘看QAQ']
	for word in text:
		bot.send_message(chat_id=update.message.chat_id, text=word)
	return
#uc_handler = CommandHandler('uc', bot_uc, pass_user_data=True)
#dispatcher.add_handler(uc_handler)

### avatar ###
def bot_avatar(bot, update, uid):
	data = profile(uid)
	if data['error'] == -1:
		bot.send_message(chat_id=update.message.chat_id, text='无法与U2娘建立神经元连接QAQ')
		return
#	elif data['error'] == 1:
#		bot.send_message(chat_id=update.message.chat_id, text='这只兔子失踪了QAQ')
	elif data['error'] == 2:
		bot.send_message(chat_id=update.message.chat_id, text='你这只傲娇不给幼兔娘看QAQ')
		return
	url = data['avatar']
	if url[0:19] == 'https://u2.dmhy.org':
		try:
			photo = requests.get(url, cookies = cookie, timeout = 3)
		except:
			bot.send_message(chat_id=update.message.chat_id, text='头像飞走了~')
			return
	else:
		try:
			photo = requests.get(url, timeout = 3)
		except:
			bot.send_message(chat_id=update.message.chat_id, text='头像飞走了~')
			return
	if photo.status_code != 200:
		bot.send_message(chat_id=update.message.chat_id, text='头像飞走了~')
		return
	open('avatar', 'wb').write(photo.content)
	avatar = open('avatar', 'rb')
	bot.sendPhoto(chat_id=update.message.chat_id, photo=avatar)
	return


### speed ###
def bot_speed(bot, update, uid):
	data = speed(uid)
	if data['error'] == -1:
		bot.send_message(chat_id=update.message.chat_id, text='无法与U2娘建立神经元连接QAQ')
		return
	if data['error'] == 1:
		bot.send_message(chat_id=update.message.chat_id, text='小钱钱飞到月球去啦~')
		return
	if data['type'] == 0:
		bot.send_message(chat_id=update.message.chat_id, text='秒收%sUCoin$_$' % (str(data['speed'])))
	else:
		bot.send_message(chat_id=update.message.chat_id, text='时薪%sUCoin QAQ' % (str(data['speed'])))
	return
#speed_handler = CommandHandler('speed', bot_speed, pass_user_data=True)
#dispatcher.add_handler(speed_handler)

### online ###
def bot_online(bot, update):
	if online():
		bot.send_message(chat_id=update.message.chat_id, text='神经元连结正常')
		return
	else:
		bot.send_message(chat_id=update.message.chat_id, text='无法与U2娘建立神经元连接QAQ')
online_handler = CommandHandler('online', bot_online)
dispatcher.add_handler(online_handler)

### chat ###
recv = ('暖被窝', '合体', '求包养', '伪娘', '中出', '早', '午', '晚', '交往', '鬼畜', '交尾', '幼兔', '求虐', '求调教', '变身', '推倒', '傲娇', '世界线')
reply = ('主人我来帮你暖被窝w', '我来组成头部~', '很遗憾！你还未有资格', '原来你是伪娘！', '既然你想中途退出U2，我就成全你了﹗', '主人，早安！已经为您准备好早饭，在楼下的小食店。', '午安', '主人，晚安了！明天再见', '我拒绝！', '给我去死两次！', '变态！讨厌死了！', '无路赛！', '啪！', 'Pia!(ｏ ‵-′)ノ”(ノ﹏<。)', '哼，自己变去吧！', 'w', 'w', 'w')

'''
def chat(bot, update, args, user_data):
	id = update.effective_user['id']
	uid = id2uid(id)
	text = ' '.join(args)
	for i in range(0, len(reply)):
		if recv[i] in text:
			bot.send_message(chat_id=update.message.chat_id, text=reply[i])
			return
	bot.send_message(chat_id=update.message.chat_id, text='幼兔娘听不懂呢QAQ')
	return
#chat_handler = CommandHandler('u', chat, pass_args=True, pass_user_data=True)
#dispatcher.add_handler(chat_handler)

### magic ###
#def bot_magic(bot, update, args)

#def bot_gift(bot, update, args):
#	uid = ' '.join(args).upper()
#	bot.send_message(chat_id=update.message.chat_id, text=transfer(uid))
#gift_handler = CommandHandler('gift', bot_gift, pass_args=True)
#dispatcher.add_handler(gift_handler)
	

#def free(bot, update, args):
#	text_caps = ' '.join(args).upper()
#	bot.send_message(chat_id=update.message.chat_id, text=str(magic(int(text_caps))))
#free_handler = CommandHandler('free', free, pass_args=True)
#dispatcher.add_handler(free_handler)
'''
