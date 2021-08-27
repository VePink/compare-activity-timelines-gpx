import pandas as pd
import numpy as np
from gpx_converter import Converter
from geopy.distance import lonlat, distance

input_GPX_file = 'C:\\Users\\Vejas\\Documents\\GitHub\\compare-activity-timelines-gpx\\input_GPXs\\Test2.gpx'
original_df = Converter(input_file=input_GPX_file).gpx_to_dataframe()
original_df.drop(columns=['altitude'], inplace=True)

start_df = original_df.iloc[::2, :]
start_df.reset_index(drop=True, inplace=True)
start_df.rename(columns={'time': 'start_time', 'longitude': 'start_long', 'latitude': 'start_lat'}, inplace=True)

end_df = original_df.iloc[1::2, :]
end_df.reset_index(drop=True, inplace=True)
end_df.rename(columns={'time': 'end_time', 'longitude': 'end_long', 'latitude': 'end_lat'}, inplace=True)

segments_df=pd.merge(start_df, end_df, left_index=True, right_index=True)


def get_traveled_distance_m(arg):
    start_long = arg[0]
    start_lat = arg[1]
    end_long = arg[2]
    end_lat = arg[3]

    start_point = (start_lat, start_long)
    end_point = (end_lat, end_long)
    delta_m = (distance(lonlat(*start_point), lonlat(*end_point)).m)
    return delta_m

segments_df['delta_d_m'] = segments_df[['start_long', 'start_lat', 'end_long', 'end_lat']].apply(get_traveled_distance_m, axis=1)



segments_df['delta_t_s'] = segments_df['end_time'] - segments_df['start_time']





#print(segments_df)
Total = segments_df['delta_t_s'].sum()
print (Total)

'''
from geopy.distance import lonlat, distance
newport_ri_xy = (-71.312796, 41.49008)
cleveland_oh_xy = (-81.695391, 41.499498)
print(distance(lonlat(*newport_ri_xy), lonlat(*cleveland_oh_xy)).km)
'''