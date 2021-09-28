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

X_axis_val = 'time_cumulative_sum'
Y_axis_val = 'dist_cumulative_sum'

print('#----------- LOOP ACTIVITY FILES -----------#')
li = []

for activity_name in activities:
    print("converting "+activity_name+" ...")

    original_df = Converter(input_file = '.\\activities_gpx\\input\\'+activity_name).gpx_to_dataframe()
    original_df['activity_name'] = activity_name

    attributes = []

    for index, row in original_df.iterrows():
        try:
            start_point = (original_df["latitude"].iloc[index], original_df["longitude"].iloc[index])
            end_point = (original_df["latitude"].iloc[index+1], original_df["longitude"].iloc[index+1])
            distance_km = geopy.distance.geodesic(start_point, end_point).km
            start_time = (original_df["time"].iloc[index])
            end_time = (original_df["time"].iloc[index+1])
            delta_time_h = (end_time-start_time)/np.timedelta64(1,'h')
            delta_height_m = original_df["altitude"].iloc[index+1]-original_df["altitude"].iloc[index]

            def get_speed(distance_km, delta_time_h):
                if delta_time_h == 0:
                    speed_kmh = 0
                elif delta_time_h > 0:
                    speed_kmh = distance_km/delta_time_h
                return speed_kmh

            attributes.append({'distance_km': distance_km,
                                'delta_time_h': delta_time_h,
                                'delta_height_m': delta_height_m,
                                'speed_kmh': get_speed(distance_km, delta_time_h)
                                })
        except IndexError:
            print('Index error detected, but it was expected and handled.')


    deltas_df = pd.DataFrame(attributes)
    result_df = pd.merge(original_df, deltas_df, left_index=True, right_index=True)

    # Cumulative sum
    result_df['dist_cumulative_sum'] = result_df.distance_km.cumsum()
    result_df['time_cumulative_sum'] = result_df.delta_time_h.cumsum()
    result_df['height_cumulative_sum'] = result_df.delta_height_m.cumsum()

    li.append(result_df)

df = pd.concat(li, axis=0, ignore_index=True)

print('#----------- PLOT -----------#')
import plotly.express as px

fig = px.line(df, x=df[X_axis_val], y=df[Y_axis_val], color=df['activity_name'],template='plotly_dark')

#X axis
fig.update_xaxes(title_text=X_axis_val)
#fig.update_xaxes(range=[0,38])
fig.update_xaxes(tick0=0, dtick=1)
#Y axis
fig.update_yaxes(title_text=Y_axis_val)
#fig.update_yaxes(range=[0,161])
fig.update_yaxes(tick0=0, dtick=5)

fig.write_html("./index.html")
fig.show()

print('#----------- REPORT -----------#')
from CLTreport.summary import report_summary
report_summary()