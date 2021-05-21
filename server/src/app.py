from flask import Flask, render_template
from matplotlib.figure import Figure
import numpy as np
import os
import mpld3
import geopandas as gpd
from tensorflow import keras
from NN.show_prediction import build_history



app = Flask(__name__)
PATH_TO_STATIC = '/static'

def build_plot():
    numbers = keras.models.load_model('./NN/covidTO.h5')
    neighbourhoods = gpd.read_file('./NN/id-shape.geojson')
    x = np.arange(0, 10, 1)
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.set_title("Toronto Neighbourhood Counts")
    axis.set_xlabel("Longitude")
    axis.set_ylabel("Latitude")
    for ID, place in zip(neighbourhoods["AREA_SHORT_CODE"], neighbourhoods['geometry']):
        x, y = place.exterior.xy
        axis.plot(x, y, label=ID    )
    html_str = mpld3.fig_to_html(fig)
    # html_str = "/images/neighbourhoods.png"

    return html_str
    

@app.route('/')
def index():
    context = {'name':'line', 'plot':build_plot()}
    return render_template('index.html', context=context)

if __name__ == '__main__':
    print('hi')
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))