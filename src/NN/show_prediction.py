import numpy as np
import datetime as dt
from tensorflow import keras
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry.polygon import Polygon
from shapely.geometry import Point
import numpy as np

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
    
    try:
        


print("What date would you like to see?")
year = int(input("year: 2020 or 2021? "))
month = int(input("month (1-12) "))
year = int(input("day (1-31) "))


