'''
Play with the data, see what it looks like.
Make nice plots of the x-,y-,z-axis accelerometer data.
Everything is in m/s^2.
'''
import sys
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime

# experiment.py logfile event_type

def main():
	event_type = sys.argv[2]  # eg 'swipe'
	try:
		filename = sys.argv[1]
		df = pd.read_csv(filename)	
	except FileNotFoundError:
		print('Error: file does not exist')
		quit()

	
	num_events = int(df['event'].max())

	events = []
	fig = go.Figure()
	for i in range(num_events):
		cur = df.loc[df['event'] == i+1]
		
		new = pd.DataFrame(columns = ['timestamp','dx','dy','dz'])
		prev = None
		for index, record in cur.iterrows():
			if prev is not None:
				timestamp = record.timestamp
				dx = record.x - prev.x
				dy = record.y - prev.y
				dz = record.z - prev.z
				new.loc[index-1] = [timestamp, dx, dy, dz]
			prev = record
			
		events.append({'type': event_type,
			       'dx': new.dx.values.tolist(),
			       'dy': new.dy.values.tolist(),
			       'dz': new.dz.values.tolist()})

		'''fig.add_trace(go.Scatter(
    			x=new['timestamp'],
    			y=new['dx'],
			mode='lines',
			line=go.scatter.Line(color='red'),
			name='x-axis'))

		fig.add_trace(go.Scatter(
	    		x=new['timestamp'],
	    		y=new['dy'],
			mode='lines',
			line=go.scatter.Line(color='blue'),
			name='y-axis'))

		fig.add_trace(go.Scatter(
			x=new['timestamp'],
			y=new['dz'],
			mode='lines',
			line=go.scatter.Line(color='green'),
			name='z-axis'))'''
	
	with open('training.csv', 'a+') as f:
		for event in events:
			f.write(event['type'] + ',' + \
				list_to_str(event['dx']) + ',' + \
				list_to_str(event['dy']) + ',' + \
				list_to_str(event['dz']) + ',' + '\n')

	#fig.update_layout(height=600, width=1150, title_text="Acceleration by axis")
	#fig.show()


def list_to_str(l):
	s = ''
	for el in l:
		s += str(el)
		s += ' '
	return s[:-1]



if __name__ == '__main__':
	main()
