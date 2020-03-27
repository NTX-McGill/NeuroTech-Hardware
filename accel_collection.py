'''
Get serial data from COM3 and save to csv logs.
For accelerometer data with accel_read.ino.

Prompt the user for data collection every three seconds.

Unplug the Arduino to stop the program and save the data.
'''

import serial
import time
import datetime

port = 'COM3'
baudrate = 9600

start = b'<'
end = b'>'


# Read incoming serial communication from Arduino
# Append timestamp here
# Reads <msg>
def read_from_arduino(s):
	while s.read() != start:
		pass

	msg = 'timestamp:' + \
		   time.strftime('%H:%M:%S', time.localtime()) + \
		  ',' + s.read_until(end)[:-1].decode('utf-8')

	
	return msg


# Wait until the serial connection is open
# params: s: Serial, serial connection to open to Arduino
#	  counter: int, times wait_for_serial has been called
#	  timeout: int, time out after this many cycles w/o finding COM3
#	  waittime: int, seconds to wait between checking COM3
def wait_for_serial(s, counter=0, timeout=3, waittime=5):
	try:
		s.open()
	except:
		# terminate the program if we've waited long enough for COM3
		counter += 1
		if counter > timeout:
			print('Connection timed out')
			quit()
		
		print('%s not found. Trying again in ' %port, end='')
		for i in range(waittime):
			print('%d...' %(waittime-i), end='')
			time.sleep(1)
		print()
		wait_for_serial(s, counter)


# Wait until the arduino sends the ready message
# Optionally (default True) prints a message when ready
def wait_for_arduino(s, printReady=True):
	msg = ''
	while msg.find('Arduino is ready') == -1:
		while s.inWaiting() == 0:
			pass
		msg = read_from_arduino(s)
	print('Connection established')


# Get the acceleration by axis from the raw accelerometer data
def parse_data(raw_data):
	vals = {}

	for axis in range(4):  # timestamp, x, y, z
		# get the key
		key = ''
		for i in range(len(raw_data)-1):
			if raw_data[i] != ':':
				key += raw_data[i]
			else:
				raw_data = raw_data[i+1:]
				break

		# get the value
		val = ''
		for i in range(len(raw_data)-1):
			if raw_data[i] != ',':
				val += raw_data[i]
			else:
				raw_data = raw_data[i+1:]
				break
		vals[key] = val
	return vals

# Take dictionary of timestamp, x, y, z
# and return record timestamp,x,y,z
def to_csv(parsed, event):
	record = str(event) + ',' + \
		 parsed['timestamp'] + ',' + \
		 parsed['x'] + ',' + \
		 parsed['y'] + ',' + \
		 parsed['z'] + '\n'
	return record


def main():
	event_num = 0
	userid = input('Enter your id: ')

	ser = serial.Serial()
	ser.baudrate = baudrate
	ser.port = port

	wait_for_serial(ser)

	# Enter the acceleration data into a csv
	with open('logs/' + userid + '_' + \
			  time.strftime('%H_%M', time.localtime()) + '.csv',
			  'w+') as log:
		wait_for_arduino(ser)

		try:
			log.write('event,timestamp,x,y,z\n')  # header
			while True:
				# Countdown
				for i in range(3):
					print(3-i)
					time.sleep(0.5)
				
				start_time = datetime.datetime.now()
				cur_time = start_time

				print('recording')
				event_num += 1
				while (cur_time - start_time).seconds < 1:
					raw_data = read_from_arduino(ser)
					record = to_csv(parse_data(raw_data), event_num)
					log.write(record)
					cur_time = datetime.datetime.now()
				print('done')

		except:
			print('serial closed')
			ser.close()

if __name__ == '__main__':
	main()
