"""
This code is for us to visualize how each ethnicity distribute in California on a geomap. This specific function is for Mixed population.

We import plotly in order to send the code to their website and do the mapping.
First, set credentials for us to send the code;
Then, read date from CSV file and extract the data we need to use;
After that, dicide how many density we want to show on the map and set each density range a different color;
Finally, log into Plotly profile to visualize the plots.

Environment:
Modules used: plotly, plotly.plotly, plotly.figure_factory, numpy, and pandas
Files used: CA_County_Eth.csv
Data used: MIXED population
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

# Dicide how many density we want to show on the map and set each density range a different color
values = np.array(df_sample_r['MIXED'].tolist())
minimum = np.min(values)
values = values + (1.01 - minimum)
values = values.tolist()
fips = df_sample_r['FIPS'].tolist()

endpts = list(np.mgrid[min(values):max(values):5j])

colorscale = ["#dcb1fb","#b967f4","#9a28eb","#6415b7","#441574","#2e124f"]
fig = ff.create_choropleth(
    fips=fips, values=values, scope=['California'], show_state_data=True,
    colorscale=colorscale, binning_endpoints=endpts, round_legend_values=True,
    plot_bgcolor='rgb(229,229,229)',
    paper_bgcolor='rgb(229,229,229)',
    legend_title='Mixed Percentage(%) by County',
    county_outline={'color': 'rgb(255,255,255)', 'width': 0.5},
    exponent_format=True,
)
py.iplot(fig, filename='Mixed_byCounty')