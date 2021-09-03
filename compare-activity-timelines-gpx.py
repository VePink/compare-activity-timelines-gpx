import pandas as pd
import numpy as np
from gpx_converter import Converter
import geopy.distance

# Configure 
GPX_title = 'Dzukija_100'
x_axis_unit = "h"
y_axis_unit = "km"


input_GPX_file = '.\\input_GPXs\\'+GPX_title+'.gpx'
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

        start_time = (original_df["time"].iloc[index])
        end_time = (original_df["time"].iloc[index+1])
        delta_time = end_time-start_time

        deltas_list.append(
            {
            'delta_dist_km': delta_dist_km,
            'delta_time': delta_time
            }
        )

    except IndexError:
         print('Index error detected, as expected.')


deltas_df = pd.DataFrame(deltas_list)

'''
print("================= DELTAS DF ===================")
print(deltas_df)
print("================ ORIGINAL DF ==================")
print(original_df)
'''

result_df = pd.merge(original_df, deltas_df, left_index=True, right_index=True)

result_df['delta_time_h'] = result_df['delta_time'] / np.timedelta64(1, x_axis_unit)

# Cumulative sum
result_df['dist_cumulative_sum'] = result_df.delta_dist_km.cumsum()
result_df['time_cumulative_sum'] = result_df.delta_time_h.cumsum()

'''
print("=================== RESULT =====================")
print(result_df)
'''

import matplotlib.pyplot as plt
ax = plt.gca()
result_df.plot(kind='line',x='time_cumulative_sum',y='dist_cumulative_sum', color='blue', ax=ax)

plt.scatter([38], [161]) #final point

x_min = 0
x_max = 40 #max(result_df['time_cumulative_sum'])
y_min = 0
y_max = 161 #max(result_df['dist_cumulative_sum'])

x_step = round((x_max-x_min)/20)
y_step = round((y_max-y_min)/20)

plt.xlim([0, x_max])
plt.ylim([0, y_max])

plt.xticks(np.arange(x_min, x_max+x_step, x_step))
plt.yticks(np.arange(y_min, y_max+y_step, y_step))

plt.title(str(GPX_title)+".gpx || "+"time: "+str(round(max(result_df['time_cumulative_sum']), 2))+" "+x_axis_unit+" | "+"dist: "+str(round(max(result_df['dist_cumulative_sum']), 2))+" "+y_axis_unit)
plt.xlabel("laikas, "+x_axis_unit)
plt.ylabel("atstumas, "+y_axis_unit)
plt.grid()
ax.get_legend().remove()

ax.patch.set_facecolor('#ababab')
ax.patch.set_alpha(0.5)

plt.show()
