import numpy as np
from tensorflow import keras
from keras.models import Sequential
import keras.layers as layers

data_file = np.load(open('split_data_full.npz', 'rb'))

batch_size = 10

model = Sequential()
model.add(layers.Conv2D(140, input_shape=(45, 45, 13), kernel_size=(3,3), activation='relu'))
model.add(layers.Flatten())
model.add(layers.Dense(250, activation='relu'))
model.add(layers.Dense(140, activation='relu'))
model.compile('adam', 'mean_squared_error')

print(model.summary())

model.fit(data_file['x_train'], data_file['y_train'], epochs=5, batch_size=batch_size)

model.save('covidTO.h5')
# model = keras.models.load_model('covidTO.h5')

# Accuracy Percision and Recall

predicts = model.predict(data_file['x_test'])

nh_acc = {nh:[] for nh in range(140)}

for x, y in zip(predicts, data_file['y_test']):
    for i in range(140):
        if y[i] == 0:
            if x[i] == 0:
                nh_acc[i].append(0)
        else:
            nh_acc[i].append(abs((x[i]-y[i])/y[i]))

nh_acc = {nh:np.mean(nh_acc[nh]) for nh in range(140)}

print('Average accuracy = {}'.format(np.mean(list(nh_acc.values()))))

model.fit(data_file['x_train'], data_file['outbreak_train'], epochs=5, batch_size=batch_size)

model.save('covidTO_outbreaks.h5')
    
outbreak_acc = {nh:{'fp':0, 'fn':0, 'tp':0} for nh in range(140)}
for x, y in zip(predicts, data_file['outbreak_test']):
    for i in range(140):
        if x[i] > 0 and y[i] > 0 or x[i] == 0 and y[i] == 0:
            nh_acc[i]['tp'] += 1
        elif x[i] <= 0 and y[i] > 0:
            nh_acc[i]['fn'] += 1
        elif x[i] > 0 and y[i] <= 0:
            nh_acc[i]['fp'] += 1

percision = []
recall = []

for nh in range(140):
    try:
        percision.append(nh_acc[nh]['tp'] / (nh_acc[nh]['tp'] + nh_acc[nh]['fp']))
    except:
        percision.append(0)
    
    try:
        recall.append(nh_acc[nh]['tp'] / (nh_acc[nh]['tp'] + nh_acc[nh]['fn']))
    except:
        recall.append(0)

print('total percision: {}   total recall {}'.format(np.mean(percision), np.mean(recall)))



