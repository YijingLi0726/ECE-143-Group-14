"""
This code is for us to visualize how each ethnicity distribute in California on a geomap. This specific function is for White population.

We import plotly in order to send the code to their website and do the mapping.
First, set credentials for us to send the code;
Then, read date from CSV file and extract the data we need to use;
After that, dicide how many density we want to show on the map and set each density range a different color;
Finally, log into Plotly profile to visualize the plots.

Environment:
Modules used: plotly, plotly.plotly, plotly.figure_factory, numpy, and pandas
Files used: CA_County_Eth.csv
Data used: WHITE population
"""

import plotly
import plotly.plotly as py
import plotly.figure_factory as ff
import numpy as np
import pandas as pd

# Set credentials
plotly.tools.set_credentials_file(username='TKKKKK', api_key='ekYjsBAHMq2ChtKrqU8k')

# Read data from CSV file and extract the data we need to use
df_sample = pd.read_csv('CA_County_Eth.csv')
df_sample_r = df_sample[df_sample['STNAME'] == 'California']

values = df_sample_r['WHITE'].tolist()
fips = df_sample_r['FIPS'].tolist()

# Dicide how many density we want to show on the map and set each density range a different color
endpts = list(np.mgrid[min(values):max(values):5j])
colorscale = ["#b7e0e4","#60a7c7","#3e6ab0","#274777","#233158","#1d1a2d"]
fig = ff.create_choropleth(
    fips=fips, values=values, scope=['California'], show_state_data=True,
    colorscale=colorscale, binning_endpoints=endpts, round_legend_values=True,
    plot_bgcolor='rgb(229,229,229)',
    paper_bgcolor='rgb(229,229,229)',
    legend_title='White Percentage(%) by County',
    county_outline={'color': 'rgb(255,255,255)', 'width': 0.5},
    exponent_format=True,
)
py.iplot(fig, filename='White_byCounty')