from build_map_training import build_extras
from preprocess import build_data_files
from model import build_models
from show_prediction import build_history
build_extras()
build_data_files()
build_models()


print("What date would you like to see?")
year = int(input("year: 2020 or 2021? "))
month = int(input("month (1-12) "))
year = int(input("day (1-31) "))
