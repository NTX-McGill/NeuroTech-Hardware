import pandas as pd
import numpy as np
import sys
from sklearn.model_selection import train_test_split

events = list()
CATEGORIES = {'clench': 0,
	      'swipe': 1}

seq_len = 44  # cut sequences to this length

dfs = [pd.read_csv(sys.argv[1]), pd.read_csv(sys.argv[2])]

for df in dfs:

	# Generate training data of form [[times, dxs, dys, dyz], event_type]
	for i in range(1, df.event.max() - 1):
		cur = df.loc[df['event'] == i+1]
		event = pd.DataFrame(columns = ['timestamp', 'dx', 'dy', 'dz'])
		prev = None

		count = 0

		for index, record in cur.iterrows():
			if count >= seq_len:
				break
			if prev is not None:
				dx = record.x - prev.x
				dy = record.y - prev.y
				dz = record.z - prev.z
				event.loc[index - 1] = [record.timestamp,
							dx, dy, dz]
			count += 1
			prev = record
		values = np.concatenate((np.concatenate((event.timestamp.values,
					 event.dx.values), axis=0),
					 np.concatenate((event.dy.values,
					 event.dz.values), axis=0)), axis=0)
		events.append([values, CATEGORIES[cur['type'].iloc[0]]])

x = [i[0] for i in events]  # timestamped accelerometer data
print(x)
'''
y = [i[1] for i in events]  # classifications


# Separate into training, test and validation sets
x_train, x_validation, y_train, y_validation = train_test_split(x, y, test_size=0.20)

print(x_train[0].shape)

#print(x_train)
print(y_train)

# Build the model
from keras.models import Sequential, load_model
from keras.layers import Dense, LSTM
from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint

model = Sequential()
model.add(LSTM(256, input_shape=(seq_len, 4)))
model.add(Dense(1, activation='sigmoid'))

adam = Adam(lr=0.001)
chk = ModelCheckpoint('best_model.pkl', monitor='val_acc', save_best_only=True, mode='max', verbose=1)
model.compile(loss='binary_crossentropy', optimizer=adam, metrics=['accuracy'])
model.fit(x_train, y_train, epochs=100, batch_size=30, callbacks=[chk], validation_data=(x_validation, y_validation))

model = load_model('best_model.pkl')

from sklearn.metrics import accuracy_scpre
test_preds = model.predict_classes(x_test)
accuracy_score(y_test, test_preds)

print(accuracy_score)'''
