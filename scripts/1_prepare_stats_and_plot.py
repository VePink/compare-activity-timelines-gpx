import pandas as pd
import numpy as np
from gpx_converter import Converter
import geopy.distance

# OPTION1 read all activities in input folder 
import glob
input_files = glob.glob('.\\activities_gpx\\input\\' + "\*.gpx")
activities = []

import os
for path_and_filename in input_files:
    filename=os.path.basename(path_and_filename)
    activities.append(filename)

# OPTION2 Manualy specify activity names
#activities = ['2x100_I','2x100_II'] 


print('#----------- LOOP ACTIVITY FILES -----------#')
li = []

for activity_name in activities:
    print("converting "+activity_name+" ...")
    input_GPX_file = '.\\activities_gpx\\input\\'+activity_name

    original_df = Converter(input_file=input_GPX_file).gpx_to_dataframe()
    original_df['activity_name'] = activity_name

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

            delta_height = original_df["altitude"].iloc[index+1] - original_df["altitude"].iloc[index]

            deltas_list.append(
                {
                'delta_dist_km': delta_dist_km,
                'delta_time_h': delta_time,
                'delta_height_m': delta_height
                }
            )

        except IndexError:
            print('Index error detected, but it was expected and handled.')


    deltas_df = pd.DataFrame(deltas_list)

    result_df = pd.merge(original_df, deltas_df, left_index=True, right_index=True)

    result_df['delta_time_h'] = result_df['delta_time_h'] / np.timedelta64(1, 'h')
    result_df['speed_kmh'] = result_df['delta_dist_km']/result_df['delta_time_h']

    # Cumulative sum
    result_df['dist_cumulative_sum'] = result_df.delta_dist_km.cumsum()
    result_df['time_cumulative_sum'] = result_df.delta_time_h.cumsum()
    result_df['height_cumulative_sum'] = result_df.delta_height_m.cumsum()

    li.append(result_df)

df = pd.concat(li, axis=0, ignore_index=True)

print('#----------- PLOT -----------#')
import plotly.express as px

fig = px.line(df, x=df['time_cumulative_sum'], y=df['dist_cumulative_sum'],color=df['activity_name'],template = 'plotly_dark')

#X axis
fig.update_xaxes(title_text='Laikas, valandos')
fig.update_xaxes(range=[0,38])
fig.update_xaxes(tick0=0, dtick=1)
#Y axis
fig.update_yaxes(title_text='Atstumas, km')
fig.update_yaxes(range=[0,161])
fig.update_yaxes(tick0=0, dtick=5)

fig.write_html("./index.html")
fig.show()

print('#----------- REPORT -----------#')
from CLTreport.summary import report_summary
report_summary()