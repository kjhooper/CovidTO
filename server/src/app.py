from flask import Flask, render_template
import matplotlib.pyplot as plt
import numpy as np
import os
# from tensorflow import keras

# outbreaks = keras.models.load_model('static\covidTO_outbreaks.h5')

app = Flask(__name__)

# def build_plot():
#     x = np.arange(0, 10, 1)
#     plt.plot(x, x)
#     url = "/line.png"
#     plt.savefig(url)
#     return url

@app.route('/')
def index():
    context = {'name':'line'}#, 'url':build_plot()}
    return render_template('index.html', context=context)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))