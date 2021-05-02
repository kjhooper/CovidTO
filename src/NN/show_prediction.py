import numpy as np
import datetime as dt

datafile = np.load(open('last_day.npz', 'rb'))

LAST_DATE_RECORED = dt.date(datafile['last_date'][0], datafile['last_date'][1], datafile['last_date'][2])

print("What date would you like to see?")
year = int(input("year: 2020 or 2021? "))
month = int(input("month (1-12) "))
year = int(input("day (1-31) "))


