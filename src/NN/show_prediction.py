import numpy as np
import datetime as dt
from tensorflow import keras
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry.polygon import Polygon
from shapely.geometry import Point
import numpy as np
import math


datafile = np.load(open('last_day.npz', 'rb'))

LAST_DATE_RECORED = dt.date(datafile['last_date'][0], datafile['last_date'][1], datafile['last_date'][2])

def build_history(date):
    template = np.load(open('map_template.npy', 'rb'))
    code_dict = pickle.load(open('n_codes.p', 'rb'))
    conversion_dict = {'Mimico (includes Humber Bay Shores)': 'Mimico', 'Danforth-East York':'Danforth East York', 'Cabbagetown-South St. James Town':'Cabbagetown-South St.James Town', 'North St. James Town':'North St.James Town', 'Briar Hill - Belgravia':'Briar Hill-Belgravia'}
    map_indicies = pickle.load(open('map_indicies.p', 'rb'))
    ones_map = np.load(open('ones_template.npy', 'rb')).reshape((1, 45, 45))

    model_counts = keras.models.load_model('covidTO.h5')
    model_outbreaks = keras.models.load_model('covidTO.h5')

    neighbourhoods = gpd.read_file('Neighbourhoods.geojson')

    index = LAST_DATE_RECORED - date
    index = index.days
    if index > 0
        try:
            days = []
            for i in range(4):
                day_input = np.zeros((3, 45,45))
                for nh in range(1, 141):
                    for x, y in zip(map_indicies[nh][0], map_indicies[nh][1]):
                        day_input[0][x, y] = datafile['y'][-index-i][nh-1]
                        day_input[1][x, y] += datafile['outbreaks'][-index-i][nh-1]
                    day_input[2] += (curr_date.isocalendar().week-1)/51
                    days.append(day_input)
            
            history = np.concatenate(days)
            data = np.concatenate((history, ones_map)).reshape((45, 45, 13))

            output_counts = model_counts.predict(data)
            output_outbreaks = model_outbreaks.predicts(data)
    elif index == 0:
        output_counts = model_counts.predict(datafile['x'])
        output_outbreaks = model_outbreaks.predict(datafile['x'])
    else:
        hsitory = datafile['x']
        y = [math.ceil(x) for x in model_counts.predict(history)]
        output_outbreaks = outbreaks = [math.ceil(x) for x in model_outbreaks.predict(history)]
        for i in range(abs(index)-1):
            day_input = np.zeros((3, 45,45))
                for nh in range(1, 141):
                    for x, y in zip(map_indicies[nh][0], map_indicies[nh][1]):
                        day_input[0][x, y] = datafile['y'][-index-i][nh-1]
                        day_input[1][x, y] += datafile['outbreaks'][-index-i][nh-1]
                    day_input[2] += (curr_date.isocalendar().week-1)/51
                    history = np.concatenate((day_input, history[:-3]))
    except:
        print('something went wrong')

