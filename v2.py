import requests
from bs4 import BeautifulSoup
from time import strftime, localtime, sleep

start_time = localtime()
with open('log/log_'+strftime("%Y-%m-%d_%H:%M:%S", start_time) +'.csv', 'a+') as f:
	f.write('time,buy,sell\n')

while(True):
	html = requests.get('https://www.exch.ktb.co.th/exchangerate/pages/travelCardRate')
	soup = BeautifulSoup(html.content, "html.parser")
	tables = soup.findChildren('table')
	my_table = tables[0]
	rows = my_table.findChildren(['th', 'tr'])
	cell = rows[6].findChildren('td')
	with open('log/log_'+strftime("%Y-%m-%d_%H:%M:%S", start_time) +'.csv', 'a+') as f:
		f.write(strftime("%Y-%m-%d_%H:%M:%S", localtime())+',')
		f.write(cell[2].string + ',')
		f.write(cell[3].string + '\n')
	sleep(60)
