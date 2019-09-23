import os
import key
import requests
from bs4 import BeautifulSoup
from time import strftime, localtime

class Log:
	def __init__(self):
		if not os.path.exists('log'):
			os.mkdir(dirName)
		self.last_mday = localtime().tm_mday
		self.filename = 'log/log_' + self.get_current_datetime()  +'.csv'
		self.write_log('time,buy,sell\n')
		
	def write_log(self, msg):
		mday = localtime().tm_mday
		if(mday != self.last_mday):
			self.last_mday = mday
			self.filename = 'log/log_' + self.get_current_datetime()  +'.csv'
			self.write_log('time,buy,sell\n')
		with open(self.filename, 'a+') as log_file:
			log_file.write(msg)

	def get_current_datetime(self):
		return strftime("%Y-%m-%d_%H:%M:%S", localtime())


class Notify:
	def __init__(self, medium='line',line_token=None):
		if(medium=='line'):
			if(line_token==None):
				print('Plz input valid line token')
				exit(1)
			self.line_init(line_token)
			self.send = lambda msg: self.line_notify(msg)

	def line_init(self, token):
		self.url = 'https://notify-api.line.me/api/notify'
		self.token = token
		self.headers = {
			'content-type': 'application/x-www-form-urlencoded',
			'Authorization': 'Bearer ' + self.token
		}

	def line_notify(self, msg):
		requests.post(
			self.url, headers=self.headers,
			data = {'message': msg})

		
class Parser:
	def __init__(self, log, src=None):
		self.notify = Notify(medium='line', line_token=key.admin_group)
		self.log = log
		if(src=='ktb'):
			self.ktb_init()
			self.parse = self.ktb_parse

	def ktb_init(self):
		self.link = 'https://www.exch.ktb.co.th/exchangerate/pages/travelCardRate'
		date, time = self.log.get_current_datetime().split('_')
		try:
			html = requests.get(self.link)
			self.notify.send('[Successfully]\nDate: {}\nTime: {}'.format(date, time))
		except Exception as e:
			self.notify.send('[Failed]\nDate: {}\nTime: {}'.format(date, time))
			print(e)
			exit(1)
			

	def ktb_parse(self):
		html = requests.get(self.link)
		parser = BeautifulSoup(html.content, "html.parser")
		table = parser.findChildren('table')[0]
		rows = table.findChildren(['th', 'tr'])
		JPY_cell = rows[6].findChildren('td')
		date = self.log.get_current_datetime()
		buy = JPY_cell[2].string
		sell = JPY_cell[3].string
		self.log.write_log(date + ',' + buy + ',' + sell + '\n')
		return date, buy, sell	
