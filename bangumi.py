import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import re
import time

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument('--disable-gpu')

executable_path = (r'D:\chromedriver.exe')
base_url = 'https://bangumi.bilibili.com/anime/timeline'

driver = webdriver.Chrome(executable_path = executable_path, chrome_options = chrome_options)
driver.get(base_url + "/")

timetable = driver.find_elements_by_class_name('day-wrap')

pattern = re.compile('\d{2}:\d{2}')

bangumi = timetable[0].text.split('\n')
temp = ''
first = 1
skip = 0
for word in bangumi:
	if pattern.match(word) is not None:
		temp += '\n'
		temp += word
		first = 1
		skip = 0
	else:
		if skip:
			skip = 0
			continue
		if first:
			temp += ' '
			temp += word
			first = 0
			skip = 1
		else:
			temp += ', '
			temp += word
			skip = 1
yesterday = temp.lstrip('\n')

bangumi = timetable[1].text.split('\n')
#print(bangumi)
temp = ''
first = 1
skip = 0
for word in bangumi:
	if pattern.match(word) is not None:
		if word == time.strftime("%H:%M", time.localtime()):
			skip = 1
			continue
		temp += '\n'
		temp += word
		first = 1
		skip = 0
	else:
		if skip:
			skip = 0
			continue
		if first:
			temp += ' '
			temp += word
			first = 0
			skip = 1
		else:
			temp += ', '
			temp += word
			skip = 1
today = temp.lstrip('\n')

bangumi = timetable[2].text.split('\n')
temp = ''
first = 1
skip = 0
for word in bangumi:
	if pattern.match(word) is not None:
		temp += '\n'
		temp += word
		first = 1
		skip = 0
	else:
		if skip:
			skip = 0
			continue
		if first:
			temp += ' '
			temp += word
			first = 0
			skip = 1
		else:
			temp += ', '
			temp += word
			skip = 1
tomorrow = temp.lstrip('\n')

print(yesterday, today, tomorrow)
with open('yesterday', 'w') as f:
	f.write(yesterday)
	f.close()

with open('today', 'w') as f:
	f.write(today)
	f.close()
	
with open('tomorrow', 'w') as f:
	f.write(tomorrow)
	f.close()

driver.close()