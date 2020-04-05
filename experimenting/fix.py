import pandas as pd

df = pd.read_csv('logs/log_13_23.csv')

event_type = 'swipe'

df['event'] = df['type']
df['type'] = df['type'].astype('str')
df['type'].values[:] = event_type

for i in range(1, int(df['event'].max()) + 1):
	event_series = df.loc[df.event.astype('int64') == i]
	start_time = event_series.timestamp.iloc[0]

	print(start_time)

	for index, record in event_series.iterrows():
		event_series.timestamp.iloc[index] -= start_time
	
	print(event_series)

	if i > 3:
		break

#df.to_csv('logs/log_13_23_fixed.csv', index=False)
