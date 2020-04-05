from gesture_utils import parse_data, to_csv
import serial_utils
import datetime
import time
import sys

# Configuration
PORT = 'COM3'
LOG_LOC = 'logs/log_'
WINDOW = 1  # recording window time, in seconds


def main():
	event_type = sys.argv[1]

	serial = serial_utils.open_serial(PORT)
	serial_utils.wait_for_board(serial)

	with open(LOG_LOC + \
		  time.strftime('%H_%M', time.locatime()) + '.csv', 'w+') as log:
		log.write('type,event,timestamp,x,y,z\n')  # write the header
		
		# Push data from the board to csv until the serial connection closes
		try:
			collect_data(serial, event_type, log)
		except:
			print('Serial connection closed')
			serial.close()


def countdown(n, dur):
	'''
	Countdown on terminal.

	params:
	  n - int, ex. n=3 counts 3...2...1...
	  dur - float, time in seconds to wait between countdown values
	'''
	for i in range(n):
		print(n-i)
		time.sleep(dur)


def collect_data(s, event_type, log, samples=None):
	'''
	Collect accelerometer data and write them to a log.

	params:
	  s- Serial object
	  event_type - str ('swipe', etc.)
	  log - log file to write to
	  samples - int, samples to take (None if infinite)
	'''
	event_num = 0

	forever_flag = False
	if samples is None:
		samples = 100
		forever_flag = True
	
	while forever_flag:
		for i in range(samples):
			countdown(n=3, dur=0.5)
			
			start_time = datetime.datetime.now()
			cur_time = start_time
			first_flag = True
			event_num += 1
			print('Go!')
			while (cur_time - start_time).seconds < WINDOW:
				parsed = parse_data(serial_utils.read(serial))
				if first_flag:
					event_start = int(parsed[2])
					first_flag = False
				record = to_csv(parsed,
						event_num,
						event_type,
						event_start)
				log.write(record)
				cur_time = datetime.datetime.now()
				print('Done')
	print("You're done! Thanks for helping with data collection!")
	quit()


if __name__ == '__main__':
	main()
