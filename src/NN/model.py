import numpy as np
from tensorflow import keras
from keras.models import Sequential
import keras.layers as layers

data_file = np.load(open('split_data.npz', 'rb'))

batch_size = 10

model = Sequential()
model.add(layers.Conv2D(140, input_shape=(45, 45, 13), kernel_size=(3,3), activation='relu'))
model.add(layers.Flatten())
model.add(layers.Dense(250, activation='relu'))
model.add(layers.Dense(140, activation='relu'))
model.compile('adam', 'mean_squared_error')

print('Model Summary')
print(model.summary())

print('Training Covid Case Count Model')
model.fit(data_file['x_train'], data_file['y_train'], epochs=5, batch_size=batch_size)

# model.save('covidTO.h5')


model2 = Sequential()
model2.add(layers.Conv2D(140, input_shape=(45, 45, 13), kernel_size=(3,3), activation='relu'))
model2.add(layers.Flatten())
model2.add(layers.Dense(250, activation='relu'))
model2.add(layers.Dense(140, activation='relu'))
model2.compile('adam', 'mean_squared_error')


print('Training Covid Outbreaks Model')
model2.fit(data_file['x_train'], data_file['outbreak_train'], epochs=5, batch_size=batch_size)

model2.save('covidTO_outbreaks.h5')

# Accuracy Percision and Recall Analysis
model = keras.models.load_model('covidTO.h5')
model2 = keras.models.load_model('covidTO.h5')

predicts = model.predict(data_file['x_test'])


nh_acc = {nh:[] for nh in range(140)}

for x, y in zip(predicts, data_file['y_test']):
    for i in range(140):
        if y[i] == 0:
            if x[i] == 0:
                nh_acc[i].append(0)
            else:
                nh_acc[i].append(abs((y[i]-x[i])/x[i]))
        else:
            nh_acc[i].append(abs((x[i]-y[i])/y[i]))

nh_acc = {nh:np.mean(nh_acc[nh]) for nh in range(140)}

print('Average accuracy = {}'.format(np.mean(list(nh_acc.values()))))

outbreak_predicts = model2.predict(data_file['x_test'])

    
outbreak_acc = {nh:{'fp':0, 'fn':0, 'tp':0} for nh in range(140)}
for x, y in zip(outbreak_predicts, data_file['outbreak_test']):
    for i in range(140):
        if x[i] > 0 and y[i] > 0 or x[i] == 0 and y[i] == 0:
            outbreak_acc[i]['tp'] += 1
        elif x[i] <= 0 and y[i] > 0:
            outbreak_acc[i]['fn'] += 1
        elif x[i] > 0 and y[i] <= 0:
            outbreak_acc[i]['fp'] += 1

percision = []
recall = []

for nh in range(140):
    try:
        percision.append(outbreak_acc[nh]['tp'] / (outbreak_acc[nh]['tp'] + outbreak_acc[nh]['fp']))
    except:
        percision.append(0)
    
    try:
        recall.append(outbreak_acc[nh]['tp'] / (outbreak_acc[nh]['tp'] + outbreak_acc[nh]['fn']))
    except:
        recall.append(0)

print('average percision: {}   average recall {}'.format(np.mean(percision), np.mean(recall)))



