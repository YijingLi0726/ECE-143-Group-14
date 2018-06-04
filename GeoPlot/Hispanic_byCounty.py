import plotly
import plotly.plotly as py
import plotly.figure_factory as ff
import numpy as np
import pandas as pd

plotly.tools.set_credentials_file(username='TKKKKK', api_key='ekYjsBAHMq2ChtKrqU8k')
df_sample = pd.read_csv('CA_County_Eth.csv')
df_sample_r = df_sample[df_sample['STNAME'] == 'California']

values = df_sample_r['HISPANIC'].tolist()
fips = df_sample_r['FIPS'].tolist()

endpts = list(np.mgrid[min(values):max(values):4j])
# colorscale = ["#550909","#720000","#8E1010","#AB2626","#C74242",
            #   "#E46565","#FF8E8E","#FFABAB","#FFC7C7","#FFE4E4"]
colorscale = ["#FFE4E4","#FFABAB","#E46565","#AB2626","#720000"]
fig = ff.create_choropleth(
    fips=fips, values=values, scope=['California'], show_state_data=True,
    colorscale=colorscale, binning_endpoints=endpts, round_legend_values=True,
    plot_bgcolor='rgb(229,229,229)',
    paper_bgcolor='rgb(229,229,229)',
    legend_title='Hispanic Percentage(%) by County',
    county_outline={'color': 'rgb(255,255,255)', 'width': 0.5},
    exponent_format=True,
)
py.iplot(fig, filename='Hispanic_byCounty')