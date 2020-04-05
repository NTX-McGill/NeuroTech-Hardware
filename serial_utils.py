'''
Useful functions for development board-serial communication.
'''

import serial
import time


def read(s, start=b'<', end=b'>', encoding='utf-8'):
	'''
	Read incoming serial communication from dev board.
	
	params:
	  s - Serial object
	  start - byte string, to signal start of message
	  end - byte string, to signal end of message
	  encoding - str, type of encoding expected for read str

	returns: decoded str, between specified start and end bytes

	'''
	while s.read() != start:
		pass

	return s.read_until(end)[:-1].decode(encoding)


def open_serial(port, baudrate=9600, timeout=3, waittime=5):
	'''
	Attempt to open a serial connection.

	params:
	  port - str, serial port to open connection at
	  baudrate - int, rate of communication at serial port
	  timeout - int, number of wait cycles to try before timing out
	  waittime - int, seconds to wait between checking serial port

	returns: Serial object

	'''

	s = serial.Serial()
	s.port = port
	s.baudrate = baudrate

	def __open_serial__(counter):
		'''
		Keep checking the serial port until a connection is available
		or counter > timeout.

		params:
		  counter - int, number of times this function has been called
		'''
		try:
			s.open()
		except:
			if counter >= timeout:
				print('Connection timed out')
				quit()
		
			print('%s not found. Trying again in ' %s.port, end='')
			for i in range(waittime):
				print('%d...' %(waittime-i), end='')
				time.sleep(1)
			print()
			__open_serial__(counter+1)
	
	__open_serial__(0)
	return s


def wait_for_board(s, ready_message='Ready', print_ready=True):
	'''
	Wait until the dev board sends the ready_message.

	params:
	  s - Serial object
	  ready_message - str, indicates the board is ready for instructions
	  print_ready - bool, if true, print 'connection established' when done
	'''
	msg = ''
	while msg.find(ready_message) == -1:
		while s.inWaiting() == 0:
			pass
		msg = read(s)
	
	if print_ready:
		print('Connection established')


def write(s, data, encode=True, encoding='utf-8'):
	'''
	Write the data (optionally encoded) to the specified Serial object.

	params:
	  s - Serial object
	  data - str, to write to Serial
	  encode - bool, if true then encode with specified encoding before writing
	  encoding - str, type of encoding to use
	'''

	if encode:
		data.encode(encoding)
	s.write(data)
