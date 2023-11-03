import pandas as pd
import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
from datetime import date, datetime
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/D', name="Procurement Insight", external_stylesheets=[dbc.themes.BOOTSTRAP],order=5)

####################### LOAD DATASET #############################
df1 = pd.read_csv('D1_2.csv', encoding='cp1252')
df3 = pd.read_csv('D3.csv', encoding='cp1252')

####################### PAGE LAYOUT #############################
#a = date.today()
#today = a.strftime("%Y-%m-%d") #'today' will change according to the real time
today ='2023-10-23' #Assuming today is 23 Oct 2023

#for D1
x = len(df1[(df1['End_Date'] >= today ) &
            (df1['Start_Date'] <= today) &
            (df1['Procurement_Type'] == 'Jasa')])
y = len(df1[(df1['End_Date'] > today ) &
            (df1['Start_Date'] <= today) &
            (df1['Procurement_Type'] == 'Barang')])

#for D2
dff1 =  df1.loc[(df1['End_Date'] >= today ) & (df1['Start_Date'] <= today)]
dfff1 = dff1.groupby(['Oil_and_Gas_Company'])['Oil_and_Gas_Company'].count().reset_index(name='count')
dfff1_sort = dfff1.sort_values(by='count', ascending=False).head(10)

#for D3
dff3 = df3.sort_values(by='Month', ascending=False).head(12) 

#Content
heading = html.Header('Centralized Integrated Vendor Database', style={'textAlign': 'center', 'fontSize': '24px', 'color': 'white', 'backgroundColor': 'black', 'padding': '10px'})

title = [
   dbc.Col(html.H1('D. PROCUREMENT ANNOUNCEMENT INSIGHT',  style={'color': 'blue', 'fontSize': 17,'textAlign': 'left'}), align='left')
]

no1 = dbc.CardBody(
        [
            html.H4(x, style={'color': 'blue', 'fontSize': 70,'textAlign': 'center'}),
            html.P('Active Services Procurements', style={'color': 'black', 'fontSize': 20,'textAlign': 'center'}),
        ])

no2 = dbc.CardBody(
        [
            html.H4(y, style={'color': 'orange', 'fontSize': 70,'textAlign': 'center'}),
            html.P('Active Goods Procurements', style={'color': 'black', 'fontSize': 20,'textAlign': 'center'}),
        ])

#cards
card1 =dbc.Card(no1, color="light")

card2 = dbc.Card(no2, color='light') 

#column
cards = [
    dbc.Col(card1, width=4),
    dbc.Col(card2, width=4)
]


#layout
layout = dbc.Container([
    #dbc.Row(heading, justify='start'),
    
    dbc.Row(title, justify='start'),
    
    dbc.Row(
            cards,
            justify="center",
    ),


    dbc.Row([
        dbc.Col(dcc.Graph(id='mygraph1'), width=6),
        dbc.Col(children= dcc.Graph(id='mygraph2'), style={'color': 'blue', 'fontSize': 30}, width=6)
        ]),
        

    dcc.Interval(
        id='interval-1-component',
        interval=1*1000*60*10,  # every 10 mins
        n_intervals=0)
])

#callback for graph 1
@callback([Output('mygraph1', 'figure'),
               Output('mygraph1', 'config')],
              [Input('interval-1-component', 'n_intervals')])

def update_mygraph1(n):
    fig = px.bar(dfff1_sort, x = 'count', y = 'Oil_and_Gas_Company', orientation='h', title='Top 10 Oil & Gas Company with Active Tender Announcement') #need fix
    fig.update_xaxes(title_text='Number of Tender Announcement')
    fig.update_yaxes(title_text='Oil and Gas Company')
    fig.update_traces(marker=dict(color="RoyalBlue"))
    fig.update_layout(yaxis={'categoryorder':'total ascending'})

    config = {'staticPlot': False}
    return fig, config

#callback for graph 2
@callback([Output('mygraph2', 'figure'),
               Output('mygraph2', 'config')],
              [Input('interval-1-component', 'n_intervals')])
def update_mygraph2(n):
    fig = px.line(dff3, x = 'Month', y = 'Number of Tender', title='Monthly Historical Active Tender Pattern')
    fig.update_xaxes(title_text='Month')
    fig.update_yaxes(title_text='Number of Tender')
    fig.update_traces(line_color='RoyalBlue')

    config = {'staticPlot': False}
    return fig, config
