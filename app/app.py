# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import json
import pandas as pd
from pyproj import Proj, transform
from dash import Dash, html, dcc
import plotly.express as px
import plotly.graph_objects as go

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app = Dash(__name__)

counties_filename = 'data/Counties_and_Unitary_Authorities_transformed.geojson'
with open(counties_filename) as response:
    counties = json.load(response)

df_hpi = pd.read_csv('data/UK-HPI-full-file-2023-01.csv', parse_dates=['Date'], dayfirst=True)
df_hpi = df_hpi[df_hpi['Date']=='01-01-2023']
df_hpi = df_hpi[[
    'Date',
    'AreaCode',
    'AveragePrice'
]]
print(df_hpi)

print(counties.keys())

columns=['id','name', 'value'] 
df = pd.DataFrame(columns=columns)
for county in counties['features']:
    row = pd.DataFrame({
        'id': [county['id']],
        'code': [county['properties']['CTYUA22CD']],
        'name': [county['properties']['CTYUA22NM']]
    })
    df = pd.concat([df, row])

df = pd.merge(df, df_hpi, left_on='code', right_on='AreaCode', validate='1:1', how='left')

print(df)

z_col = 'AveragePrice'

fig = go.Figure(go.Choroplethmapbox(
    geojson=counties,
    locations=df['id'], 
    z=df[z_col], # z=df.unemp,
    text=df['name'],
    colorscale="Viridis", 
    zmin=df[z_col].min(),
    zmax=df[z_col].max(),
    marker_opacity=0.5,
    marker_line_width=0)
)
fig.update_layout(
    title_text='',
    mapbox_style="carto-positron",
    mapbox_zoom=4.4,
    mapbox_center = {"lat": 54.093409, "lon": -2.89479},
    height=500
)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})


app.layout = html.Div(children=[
    # html.H1(children='Hello Dash',
    #         style={
    #         'textAlign': 'center',
    #         'color': colors['text'],
    #         'height':'10vh'
    #     }),

    # html.Div(children='''
    #     Dash: A web application framework for your data.
    # '''),

    dcc.Graph(
        id='example-graph',
        figure=fig,
        style={
            'height':'100vh'
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)