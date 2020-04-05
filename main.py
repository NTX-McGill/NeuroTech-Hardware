'''
Serial communication to send model predictions (which finger moved) to the
development board to trigger haptic feedback. Also reads raw accelerometer data
from the board and sends to the gesture classification model.
'''
from gesture_utils import parse_data
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
		send_to_model(parse_data(serial_utils.read(serial)))


def send_to_model(parsed):
	'''
	@TODO
	Send accelerometer data to the model through SocketIO.

	params:
	  parsed - int list, [timestamp,x_accel,y_accel,z_accel]

	'''
	pass


def get_new_prediction():
	'''
	@TODO
	Fetch new model prediction from SocketIO.

	returns: int, prediction (or None if no prediction)
	'''
	pass


if __name__ == '__main__':
	main()
