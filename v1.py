import requests
from bs4 import BeautifulSoup
from time import strftime, localtime, sleep

start_time = localtime()
with open('log/log_'+strftime("%Y-%m-%d_%H:%M:%S", start_time) +'.txt', 'a+') as f:
	f.write('{:=^50}'.format(' '+strftime("%Y %m %d %H:%M:%S", start_time)+' '))

while(True):
	html = requests.get('https://www.exch.ktb.co.th/exchangerate/pages/travelCardRate')
	soup = BeautifulSoup(html.content, "html.parser")
	tables = soup.findChildren('table')
	my_table = tables[0]
	rows = my_table.findChildren(['th', 'tr'])
	cell = rows[6].findChildren('td')
	with open('log/log_'+strftime("%Y-%m-%d_%H:%M:%S", start_time) +'.txt', 'a+') as f:
		f.write('\n\n')
		f.write('{:-^30}\n'.format(' '+strftime("%Y-%m-%d_%H:%M:%S", localtime())+' '))
		f.write('Buy:  ' + cell[2].string + '\n')
		f.write('Sell: ' + cell[3].string + '\n')
	sleep(60)
