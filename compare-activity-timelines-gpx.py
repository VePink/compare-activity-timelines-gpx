import pandas as pd
import numpy as np
from gpx_converter import Converter
from geopy.distance import lonlat, distance

input_GPX_file = 'C:\\Users\\Ve\\Documents\\GitHub\\compare-activity-timelines-gpx\\input_GPXs\\test2.gpx'
original_df = Converter(input_file=input_GPX_file).gpx_to_dataframe()
original_df.drop(columns=['altitude'], inplace=True)

deltas_list = []

for index, row in original_df.iterrows():
    try:
        start_point = (original_df["longitude"].iloc[index], original_df["latitude"].iloc[index])
        end_point = (original_df["longitude"].iloc[index+1], original_df["latitude"].iloc[index+1])
        
        delta_distance_m = (distance(lonlat(*start_point), lonlat(*end_point)).m)
        #print(delta_distance_m)

        start_time = (original_df["time"].iloc[index])
        end_time = (original_df["time"].iloc[index+1])
        
        delta_time = end_time-start_time
        #print(delta_time)

        deltas_list.append(
            {
            'delta_distance_m': delta_distance_m,
            'delta_time': delta_time
            }
        )

    except IndexError:
         print('Index error detected, as expected.')

deltas_df = pd.DataFrame(deltas_list)
print(deltas_df)



'''
import matplotlib.pyplot as plt

# gca stands for 'get current axis'
ax = plt.gca()

result_df.plot(kind='line',x='delta_time',y='delta_distance_m', color='red', ax=ax)

plt.show()
'''