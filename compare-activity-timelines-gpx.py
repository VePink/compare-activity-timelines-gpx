import pandas as pd
import numpy as np
from gpx_converter import Converter
from geopy.distance import lonlat, distance
import geopy.distance

from pyproj import Transformer
transformer = Transformer.from_crs("epsg:4326", "epsg:3346")

GPX_title = 'Dzukija_100'

input_GPX_file = 'C:\\Users\\Ve\\Documents\\GitHub\\compare-activity-timelines-gpx\\input_GPXs\\'+GPX_title+'.gpx'
original_df = Converter(input_file=input_GPX_file).gpx_to_dataframe()
original_df.drop(columns=['altitude'], inplace=True)

deltas_list = [{
            'delta_dist_km': 0.0,
            'delta_time': '0 days 00:00:00'
            }]

for index, row in original_df.iterrows():
    try:
        start_point = (original_df["latitude"].iloc[index], original_df["longitude"].iloc[index])
        end_point = (original_df["latitude"].iloc[index+1], original_df["longitude"].iloc[index+1])
        
        delta_dist_km = geopy.distance.geodesic(start_point, end_point).km
        #delta_dist_km = geopy.distance.great_circle(start_point, end_point).km
        
        #---------------------
        pt_store=transformer.transform(original_df["latitude"].iloc[index],original_df["longitude"].iloc[index])
        pt_user=transformer.transform(original_df["latitude"].iloc[index+1], original_df["longitude"].iloc[index+1])

        #delta_dist_km = np.linalg.norm(np.array(pt_user) - np.array(pt_store))/1000
        #---------------------
        #print(delta_dist_km)

        start_time = (original_df["time"].iloc[index])
        end_time = (original_df["time"].iloc[index+1])
        
        delta_time = end_time-start_time
        #print(delta_time)

        deltas_list.append(
            {
            'delta_dist_km': delta_dist_km,
            'delta_time': delta_time
            }
        )

    except IndexError:
         print('Index error detected, as expected.')


deltas_df = pd.DataFrame(deltas_list)

print("================== DELTAS =====================")
print(deltas_df)
print("================ ORIGINAL DF ==================")
print(original_df)


result_df = pd.merge(original_df, deltas_df, left_index=True, right_index=True)

result_df['delta_time_h'] = result_df['delta_time'] / np.timedelta64(1, 'm')

# Cumulative sum
result_df['dist_cumulative_sum_km'] = result_df.delta_dist_km.cumsum()
result_df['dist_cumulative_time'] = result_df.delta_time_h.cumsum()

print("=================== RESULT =====================")
print(result_df)

import matplotlib.pyplot as plt
ax = plt.gca()
result_df.plot(kind='line',x='dist_cumulative_time',y='dist_cumulative_sum_km', color='green', ax=ax)

x_min = min(result_df['dist_cumulative_time'])
x_max = max(result_df['dist_cumulative_time'])
y_min = min(result_df['dist_cumulative_sum_km'])
y_max = max(result_df['dist_cumulative_sum_km'])


x_step = 10 
y_step = 3

#take max axis value from data
plt.xlim([0, x_max+x_step])
plt.ylim([0, y_max+y_step])

#define max axis value manualy
#plt.xlim([0, 27])
#plt.ylim([0, 125])

#take max grid value from data
plt.xticks(np.arange(x_min, x_max+x_step, x_step))
plt.yticks(np.arange(y_min, y_max+y_step, y_step))

#define max grid value manualy
#plt.xticks(np.arange(0, 27, x_step))
#plt.yticks(np.arange(0, 125, y_step))

plt.title(str(GPX_title)+": per laiką nukeliautas atstumas")
plt.suptitle("time: "+str(x_max)+" | "+"dist: "+str(y_max))
plt.xlabel("laikas, minutės")
plt.ylabel("atstumas, kilometrai")
plt.grid()
ax.get_legend().remove()
plt.show()
