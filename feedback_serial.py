'''
Serial communication to send model predictions (which finger moved) to the
development board to trigger haptic feedback. Ignores incoming data.
'''
import serial_utils

# CONFIGURATION
PORT = 'COM3'  # serial port


def main():
	serial = serial_utils.open_serial(PORT)
	serial_utils.wait_for_board(serial)  # wait for 'Ready' message

	while True:
		prediction = get_new_prediction()
		if prediction is not None:
			serial_utils.write(serial, prediction)


def get_new_prediction():
	'''
	Fetch new model prediction from SocketIO.

	returns: int, prediction (or None if no prediction)
	'''
	pass


if __name__ == '__main__':
	main()
