'''
Get serial data from COM3 and save to csv logs.
For accelerometer data with accel_read.ino.

Unplug the Arduino to stop the program and save the data.
'''

import serial
import time

port = 'COM4'
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

	
	print(msg)
	
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


def write_to_serial(s, data):
	s.write(data.encode('utf-8'))

def main():
	ser = serial.Serial()
	ser.baudrate = baudrate
	ser.port = port

	wait_for_serial(ser)
	wait_for_arduino(ser)

	try:
		while True:	
			for f in range(3):
				read_from_arduino(ser)
				write_to_serial(ser, str(f))
				time.sleep(1)
	
	except:
			ser.close()

if __name__ == '__main__':
	main()
