import pandas as pd
import glob

path = r'./staging/statistics_DFs' # use your path
all_files = glob.glob(path + "/*.csv")

li = []

for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    li.append(df)

result_df = pd.concat(li, axis=0, ignore_index=True)

result_df.drop(['time','latitude','longitude','altitude','delta_time','delta_height_m'], axis=1, inplace=True)

result_df.to_csv('./staging/unified_DF/unified_DF.csv',encoding='utf-8',index=False)

from CLTreport.summary import report_summary
report_summary()