import pandas as pd
import plotly.express as px

df = pd.read_csv('./staging/unified_DF/unified_DF.csv')
#df = pd.read_csv('./staging/statistics_DFs/Dzukija_100.csv')


fig = px.line(df, x=df['time_cumulative_sum'], y=df['dist_cumulative_sum'],color=df['activity_name'],template = 'plotly_dark')

#X axis
fig.update_xaxes(title_text='Laikas, valandos')
fig.update_xaxes(range = [0,40])
fig.update_xaxes(tick0=0, dtick=1)
#Y axis
fig.update_yaxes(title_text='Atstumas, km')
fig.update_yaxes(range = [0,161])
fig.update_yaxes(tick0=0, dtick=5)

fig.write_html("./results/index.html")
fig.show()

from CLTreport.summary import report_summary
report_summary()