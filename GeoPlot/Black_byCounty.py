import plotly
import plotly.plotly as py
import plotly.figure_factory as ff
import numpy as np
import pandas as pd

plotly.tools.set_credentials_file(username='TKKKKK', api_key='ekYjsBAHMq2ChtKrqU8k')
df_sample = pd.read_csv('CA_County_Eth.csv')
df_sample_r = df_sample[df_sample['STNAME'] == 'California']

values = df_sample_r['BLACKQ'].tolist()
fips = df_sample_r['FIPS'].tolist()

endpts = list(np.mgrid[min(values):max(values):4j])

colorscale = ["#b7e0e4","#60a7c7","#3e6ab0","#323268","#030512"]
fig = ff.create_choropleth(
    fips=fips, values=values, scope=['California'], show_state_data=True,
    colorscale=colorscale, binning_endpoints=endpts, round_legend_values=True,
    plot_bgcolor='rgb(229,229,229)',
    paper_bgcolor='rgb(229,229,229)',
    legend_title='Black Percentage(%) by County',
    county_outline={'color': 'rgb(255,255,255)', 'width': 0.5},
    exponent_format=True,
)
py.iplot(fig, filename='Black_byCounty')