import numpy as np
import pickle
import pandas as pd
import datetime as dt
from sklearn.model_selection import train_test_split

# # df = pd.read_csv('COVID19_cases.csv', usecols="Neighbourhood Name)
# # neighbourhood_codes = {}

# # for row in pd.read_csv('COVID19_cases.csv', usecols=["Neighbourhood Name"], chunksize=1):
# #     if len(neighbourhood_codes) == 140:
# #         break
# #     name = row["Neighbourhood Name"].iloc[0]
# #     id_num = name.split()
# #     print(id_num)
#     # neighbourhood_codes[name] = neighbourhoods["AREA_SHORT_CODE"].iloc[i]

# # pickle.dump(neighbourhood_codes, open('n_codes.p', 'wb'))



# https://www.cbc.ca/news/health/typical-covid-19-progression-1.5546949 approx 7 days after symptoms you get hospitalized
template = np.load(open('map_template.npy', 'rb'))
code_dict = pickle.load(open('n_codes.p', 'rb'))
conversion_dict = {'Mimico (includes Humber Bay Shores)': 'Mimico', 'Danforth-East York':'Danforth East York', 'Cabbagetown-South St. James Town':'Cabbagetown-South St.James Town', 'North St. James Town':'North St.James Town', 'Briar Hill - Belgravia':'Briar Hill-Belgravia'}
# print(code_dict.keys())
map_indicies = pickle.load(open('map_indicies.p', 'rb'))
ones_map = np.load(open('ones_template.npy', 'rb')).reshape((1, 45, 45))

x_data = []
y_data = []
outbreak_data = []

cols = ['Assigned_ID', 'Outbreak Associated', 'Neighbourhood Name', 'Episode Date', 'Outcome', 'Ever Hospitalized']

counts = {n:0 for n in range(1, 141)}
outbreaks = {n:0 for n in range(1, 141)}
active = {}
curr_date = dt.date.fromisoformat(pd.read_csv('COVID19_cases.csv', usecols=['Episode Date'], nrows=1)['Episode Date'][0])
hist_count = 0
history = np.zeros((12, 45, 45))
make_inputs = False
make_outputs = False

count = 0

for row in pd.read_csv('COVID19_cases.csv', usecols=cols, chunksize=1):
    try:
        nh_name = row['Neighbourhood Name'].iloc[0]
        if type(nh_name) != str:
            raise TypeError
        code_dict[nh_name]
    except KeyError:
        try:
            nh_name = conversion_dict[row['Neighbourhood Name'].iloc[0]]
            code_dict[nh_name]
        except KeyError:
            print(nh_name)
            

        ep_date = dt.date.fromisoformat(row['Episode Date'].iloc[0])
        counts[code_dict[nh_name]] += 1


        if row['Outcome'].iloc[0] == 'FATAL' or row['Ever Hospitalized'].iloc[0]=='Yes':
            ep_date += dt.timedelta(weeks=1)
        else:
            ep_date += dt.timedelta(weeks=2)
        
        if ep_date not in active:
            active[ep_date] = {code_dict[nh_name]: 1}
        else:
            if not code_dict[nh_name] in active[ep_date]:
                active[ep_date][code_dict[nh_name]] = 1
            else:
                active[ep_date][code_dict[nh_name]] += 1
        
        if ep_date in active:
            for key in active[ep_date].keys():
                counts[key] -= active[ep_date][key]
            active.pop(ep_date)
        if row['Outbreak Associated'].iloc[0] == 'Outbreak Associated':
            outbreaks[code_dict[nh_name]] = 1

        
        if curr_date != dt.date.fromisoformat(row['Episode Date'].iloc[0]):
            curr_date = dt.date.fromisoformat(row['Episode Date'].iloc[0])

            if make_inputs:
                x_data.append(np.concatenate((history, ones_map)).reshape((45, 45, 13)))
                # print(np.shape(np.concatenate((history, ones_map))))
                if make_outputs:
                    output = list(counts.items())
                    outbreak_out = list(outbreaks.items())
                    output.sort()
                    outbreak_out.sort()
                    output = np.array([item[1] for item in output])
                    outbreak_out = np.array([item[1] for item in outbreak_out])
                    y_data.append(output)
                    outbreak_data.append(outbreak_out)

                    # print(np.shape(output)
            elif not make_inputs and hist_count == 4:
                make_inputs = True
                make_outputs = True

            else:
                hist_count += 1

            day_input = np.zeros((3, 45,45))
            for key in counts.keys():
                for x, y in zip(map_indicies[key][0], map_indicies[key][1]):
                    day_input[0][x, y] = counts[key]

                day_input[1][x, y] += outbreaks[key]
                day_input[2] += (curr_date.isocalendar().week-1)/51
            
            history = np.concatenate((day_input, history[:-3]))

            outbreaks = {n:0 for n in range(1, 141)}
            print(curr_date)
    except TypeError:
        pass

# x_train, x_test, y_train, y_test = train_test_split(data['x'], data['y'], shuffle=False)
x_train, x_test, y_train, y_test, outbreak_train, outbreak_test = train_test_split(x_data, y_data, outbreak_data, shuffle=False)

np.savez_compressed(open('split_data_full.npz', 'wb'), x_train=x_train, y_train=y_train, x_test=x_test, y_test=y_test, outbreak_train=outbreak_train, outbreak_test=outbreak_test)