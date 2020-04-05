'''
Functions for accelerometer gesture data collection from the development board.
'''


# Get the acceleration by axis from the raw accelerometer data
def parse_data(raw_data):
	'''
	Parse the raw accelerometer data (remove spaces, split by ',').

	params:
	  rawdata - str, raw output from development board

	returns: int list
	'''
	return [int(el) for el in raw_data.replace(' ', '').split(',')]


# Take dictionary of timestamp, x, y, z
# and return record timestamp,x,y,z
def to_csv(parsed, event, event_type, event_start):
	'''
	Take parsed raw_data (str list) and put into csv format.
	
	params:
	  parsed: int list, timestamped (millis()) accelerometer data
	  event: int, event number
	  event_type: str, gesture type ('swipe', 'none', etc.)
	  event_start: int, first millis() value from this event

	returns: csv record ('event_type,event,timestamp,x,y,z')
	'''
	record = event_type + ',' + \
		 str(event) + ',' + \
		 str(parsed[0] - event_start) + ',' + \
		 str(parsed[1]) + ',' + \	# x acceleration
		 str(parsed[2]) + ',' + \	# y acceleration
		 str(parsed[3]) + '\n'		# z acceleration
	return record
