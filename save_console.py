'''
Get serial data from COM3 and save to csv logs.
For accelerometer data with accel_read.ino.

Unplug the Arduino to stop the program and save the data.
'''

import serial
import time

start = b'<'
end = b'>'

def read_from_arduino(s):
	while s.read() != start:
		pass

	msg = 'timestamp:' + \
		   time.strftime('%H:%M:%S', time.localtime()) + \
		  ',' + s.read_until(end)[:-1].decode('utf-8')

	return msg

def wait_for_arduino(s):
	msg = ''
	while msg.find('Arduino is ready') == -1:
		while s.inWaiting() == 0:
			pass
		msg = read_from_arduino(s)

def parse_data(raw_data):
	vals = {}

	for axis in range(4):
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

def main():

	userid = input('Enter your id: ')

	port = "COM3"
	baudRate = 9600
	ser = serial.Serial(port, baudRate)

	with open('logs/' + userid + '_' + \
			  time.strftime('%H_%M', time.localtime()) + '.log',
			  'w+') as log:
		wait_for_arduino(ser)

		try:
			log.write('timestamp,x,y,z\n')
			while True:	
				raw_data = read_from_arduino(ser)
				parsed = parse_data(raw_data)
				record = parsed['timestamp'] + ',' + \
						 parsed['x'] + ',' + \
						 parsed['y'] + ',' + \
						 parsed['z'] + '\n'
				log.write(record)

		except:
			ser.close()

if __name__ == '__main__':
	main()
