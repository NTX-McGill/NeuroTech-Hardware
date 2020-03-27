'''
Make nice plots of the x-,y-,z-axis accelerometer data.
Everything is in m/s^2.
'''
import sys
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def main():
	try:
		filename = sys.argv[1]
		df = pd.read_csv(filename)	
	except FileNotFoundError:
		print('Error: file does not exist')
		quit()

	
	num_events = int(df['event'].max())
	dfs = []
	fig = go.Figure()
	for i in range(num_events):
		cur = df.loc[df['event'] == i+1]
		dfs.append(cur)

		fig.add_trace(go.Scatter(
    			x=cur['timestamp'],
    			y=cur['x'],
			mode='lines',
			name='x-axis'))

		fig.add_trace(go.Scatter(
	    		x=cur['timestamp'],
	    		y=cur['y'],
			mode='lines',
			name='y-axis'))

		fig.add_trace(go.Scatter(
			x=cur['timestamp'],
			y=cur['z'],
			mode='lines',
			name='z-axis'))
		
	


	
	'''
	# Reverse because upside down on person
	df['x'] = df['x'].map(lambda q : -q)
	df['y'] = df['y'].map(lambda q : -q)
	#df['z'] = df['z'].map(lambda q : -q)

	fig = go.Figure()

	fig.add_trace(go.Scatter(
    		x=df['timestamp'],
    		y=df['x'],
		mode='lines',
		name='x-axis'))

	fig.add_trace(go.Scatter(
	    	x=df['timestamp'],
	    	y=df['y'],
		mode='lines',
		name='y-axis'))

	fig.add_trace(go.Scatter(
		x=df['timestamp'],
		y=df['z'],
		mode='lines',
		name='z-axis'))
	'''

	fig.update_layout(height=600, width=1150, title_text="Acceleration by axis")
	fig.show()


if __name__ == '__main__':
	main()
