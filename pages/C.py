import pandas as pd
import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import json

px.defaults.template = "ggplot2"

dash.register_page(__name__, path='/C', name="Map", order=4)

with open('indonesia-province.json', 'r') as json_file:
  geojson = json.load( json_file)



# donwload vendor data
df = pd.read_csv('C4_ID.csv',delimiter=';')
radioitems_options = ['Small_Medium','Large']




layout = html.Div([
  dcc.RadioItems(id='business_size', options = radioitems_options, value = 'Small_Medium'),
  dcc.Graph(id="cloropleth_map")
  ])

@callback(
  Output('cloropleth_map','figure'),
  Input ('business_size','value')
  )

def update_graph(business_size_option):

  if business_size_option == 'Small_Medium':
    filtered_df = df['Small_Medium']
  if business_size_option == 'Large':
    filtered_df = df['Large']

  colorscale = ["#f7fbff", "#ebf3fb", "#deebf7", "#d2e3f3", "#c6dbef", "#b3d2e9", "#9ecae1",
    "#85bcdb", "#6baed6", "#57a0ce", "#4292c6", "#3082be", "#2171b5", "#1361a9",
    "#08519c", "#0b4083", "#08306b"]

  fig = px.choropleth(df,geojson =geojson, 
    locations ="Province", 
    color = filtered_df,
    featureidkey = "properties.Propinsi")
    #title={"Number of Small & Medium Companies in Indonesian Provinces":title, 'x':0.5, 'xanchor':'center'})

    
  fig.update_geos(fitbounds="locations", visible=False)
  #https://plotly.com/python/reference/choropleth/
  #fig.update_traces(colorscale=[[0, 'rgb(0,0,255)'], [1, 'rgb(255,0,0)']], selector=dict(type='choropleth'))
  #fig.update_traces(colorscale=[[0, 'Bluered'], [1, 'Blues']], selector=dict(type='choropleth'))
  fig.update_traces(colorscale=colorscale, selector=dict(type='choropleth'))

  #fig.update_traces(geo=filtered_df, selector=dict(type='choropleth'))
# fig.update_traces(geojson=geojson,
#                             locations="Province",
#                             text=filtered_df,
#                             textfont=dict(size=8, color='red'),
#                             mode='text')

    
  fig.update_layout(margin={"r":0,"t":100,"l":0,"b":0})
  fig.update_layout(title_text= f'Number of {business_size_option} Companies in Indonesian Provinces', title_x=0.5)

  return fig

# Create a cloropleth Map 



projections = 'mercator'
