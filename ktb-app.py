import key
from local_lib import Log, Parser, Notify
from time import sleep

if __name__ == '__main__':
	log = Log()
	parser = Parser(log=log, src='ktb')
	# notify = Notify(medium = 'line', line_token = key.testing_group)
	notify = Notify(medium = 'line', line_token = key.japan_group)
	admin = Notify(medium = 'line', line_token = key.admin_group)

	mid_range = False
	low_range = False

	last_h = -1
	sell_data = []
	
	while True:
		datetime, buy, sell = parser.parse()
		sell_data.append(float(sell))
		
		date, time = datetime.split('_')
		Y,M,D = date.split('-')
		date = ' '.join([D,M,Y])
		if (float(sell) <= 0.2815 and not low_range):
			notify.send('\nDate: {}\nTime: {}\nBuy: {}\nSell: {}'.format(date,time, buy, sell))	
			low_range = True
			mid_range = False
		elif (float(sell) > 0.2815 and float(sell) <= 0.2820 and not mid_range):
			notify.send('\nDate: {}\nTime: {}\nBuy: {}\nSell: {}'.format(date,time, buy, sell))
			low_range = False
			mid_range = True
		elif (float(sell) > 0.2820):
			low_range = False
			mid_range = False
		last_sell = sell
		h,m,s = time.split(':')
		try:
			if(int(h) in [0]+list(range(8,24)) and last_h != h and last_h != -1):
				summary =  '\n[Summary] Statistics\nDate: {}\nTime: {}'.format(date, time)
				summary += '\nMax: {}\nMin: {}\nAvg: {:.6f}'.format(max(sell_data),min(sell_data),sum(sell_data)/len(sell_data))
				summary += '\nCount data: {}'.format(len(sell_data))
				admin.send(summary)
				sell_data = []
		except Exception as e:
			print('----MAIN ERROR----')
			print(e)
			print('--END MAIN ERROR--')
		last_h = h
		sleep(59)
