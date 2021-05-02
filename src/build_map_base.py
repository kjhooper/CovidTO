import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry.polygon import Polygon
from shapely.geometry import Point
import numpy as np
import pickle


neighbourhoods = gpd.read_file('Neighbourhoods.geojson')

img_size = 45

x, y = neighbourhoods['geometry'][0].exterior.xy

min_x = min(x)
max_x = max(x)
min_y = min(y)
max_y = max(y)

for place in neighbourhoods['geometry'][1:]:
    x, y = place.exterior.xy
    if min(x) < min_x:
        min_x = min(x)
    if max(x) > max_x:
        max_x = max(x)
    if min(y) < min_y:
        min_y = min(y)
    if max(y) > max_y:
        max_y = max(y)


x_pts = np.linspace(min_x, max_x, img_size)
y_pts = np.linspace(min_y, max_y, img_size)

# # X, Y = np.meshgrid(x_pts, y_pts)

# # plt.plot(x_pts, y_pts, 'o')
# # for place in neighbourhoods['geometry']:
# #     x, y = place.exterior.xy
# #     plt.plot(x, y)
# # plt.show()

neighbourhood_arr = np.zeros((img_size, img_size))
ones_arr = np.zeros((img_size, img_size))
neighbourhood_codes = {}

for i in range(140):
    name = neighbourhoods["AREA_NAME"].iloc[i].split(' (')[0]
    neighbourhood_codes[name] = neighbourhoods["AREA_SHORT_CODE"].iloc[i]

pickle.dump(neighbourhood_codes, open('n_codes.p', 'wb'))

# for i in range(45):
#     for j in range(45):
#         point = Point(x_pts[i], y_pts[::-1][j])
#         for loc in range(140):
#             if neighbourhoods['geometry'].iloc[loc].contains(point):
#                 neighbourhood_arr[i, j] += neighbourhoods['AREA_SHORT_CODE'].iloc[loc]
#                 ones_arr[i, j] += 1
#                 break
# # print(neighbourhood_arr)

# ones_arr = np.rot90(ones_arr)

# np.save(open('ones_template.npy', 'wb'), ones_arr)
# neighbourhood_arr = np.rot90(neighbourhood_arr)

# np.save(open('map_template.npy', 'wb'), neighbourhood_arr)

# # plt.imshow(neighbourhood_arr, extent=[min_x, max_x, min_y, max_y], origin='lower')
# # # plt.plot(X, Y, 'o')
# # for place in neighbourhoods['geometry']:
# #     x, y = place.exterior.xy
# #     plt.plot(x, y)
# # plt.show()

# print(np.load(open('map_template.npy', 'rb')))
# print(pickle.load(open('n_codes.p', 'rb')))

# maps = np.load(open('map_template.npy', 'rb'))
# d = pickle.load(open('n_codes.p', 'rb'))

# index_dict = {}

# for i in range(1, 141):
#     indicies = np.where(maps==i)
#     index_dict[i] = [indicies[0], indicies[1]]
# pickle.dump(index_dict, open('map_indicies.p', 'wb'))