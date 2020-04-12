'''
Serial communication to send model predictions (which finger moved) to the
development board to trigger haptic feedback. Also reads raw accelerometer data
from the board and sends to the gesture classification model.

Client for SocketIO server.
'''
from gesture_utils import parse_data
import serial_utils
import socketio

# CONFIGURATION
PORT = 'COM3'  # serial port
SERVER = 'https://localhost:4002'


def main():
	serial = serial_utils.open_serial(PORT)
	serial_utils.wait_for_board(serial)  # wait for 'Ready' message

	# Setup socketio
	sio = socketio.Client()

	@sio.event
	def connect():
		print('server connection established')

	@sio.on('Finger')
	def get_prediction(prediction):
		print('received ', prediction)

		# Try writing the prediction to the board
		try:
			serial_utils.write(serial, prediction)
		except:
			serial.close()
			print('serial connection closed')

	
	@sio.on('Update')
	def send_accel_to_model():
		'''
		Send accelerometer data to the model through SocketIO.
		Send when pinged.

		params:
		  parsed - int list, [timestamp,x_accel,y_accel,z_accel]
	
		'''
		# Try reading the accelerometer data from Serial
		try:
			sio.emit('accel_event', {'accel_data': parse_data(serial_utils.read(serial))}
		except:
			serial.close()
			print('serial connection closed')

	
	@sio.event
	def disconnect():
		print('disconnected from server')


	sio.connect(SERVER)
	sio.wait()


if __name__ == '__main__':
	main()
