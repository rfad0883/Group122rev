import pandas as pd
import dash
from dash import html, dash_table, dcc, callback
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from datetime import datetime, timedelta
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/B', name="Vendor Performance", order=3)

####################### LOAD DATASET #############################


####################### PAGE LAYOUT #############################
# C1 Chart Preparation
df_c1 = pd.read_csv('C11.csv')
df_c1['End of Certificate'] = pd.to_datetime(df_c1['End of Certificate'])
today = datetime.now()
six_months_later = today + timedelta(days=6*30)  # Approximating a month as 30 days
df_filtered = df_c1[(df_c1['End of Certificate'] >= today) & (df_c1['End of Certificate'] <= six_months_later)]
df_filtered['Month-Year'] = df_filtered['End of Certificate'].dt.strftime('%b-%y')
certificate_counts = df_filtered['Month-Year'].value_counts().sort_index()

# C2 Chart Preparation
df_c2 = pd.read_csv('C22.csv')
df_c2 = df_c2.dropna(subset=['Year'])
df_c2['Year'] = df_c2['Year'].astype(int)
df_c2['Alias'] = df_c2['Alias'].fillna(method='ffill')
df_c2['No'] = df_c2['No'].fillna(method='ffill')

# C3 Chart Preparation
df_c3 = pd.read_csv('C33.csv')
df_c3 = df_c3.dropna(subset=['Years'])
df_c3['Years'] = df_c3['Years'].astype(int)

# Initialize the Dash app
app = dash.Dash(__name__)

#content

title = html.H1('B. VENDOR PERFORMANCE INSIGHT',  style={'color': 'blue', 'fontSize': 17,'textAlign': 'left'})
dateassumption = datetime(2023, 9, 13)
currentdate = html.H1(f"Date: {dateassumption.strftime('%d-%m-%Y')}", style = {"textAlign":"start","font-size":"16px"}),
graph_c3 = dcc.Graph(id='c3-chart', figure={
            'data': [
                go.Scatter(x=df_c3['Years'], y=df_c3['Registered'], mode='lines+markers', name='Registered', line=dict(width=4)),
                go.Scatter(x=df_c3['Years'], y=df_c3['Has Valid Certificate'], mode='lines+markers', name='Has Valid Certificate', line=dict(width=4))
            ],
            'layout': go.Layout(
                title='Number of Vendors in Five Years',
                xaxis=dict(title='Year'),
                yaxis=dict(title='Number of Vendors'),
                hovermode='x unified',
                font=dict(family="Arial, sans-serif", size=14, color="black")
            )
})


layout = dbc.Container([
    # Main Title
    #dbc.Row (head),
    dbc.Row (title),
    
    html.Div([
        dcc.Graph(id='c1-chart', figure={
            'data': [
                go.Bar(x=certificate_counts.index, y=certificate_counts.values, marker_color='RoyalBlue')
            ],
            'layout': go.Layout(
                title="Number of Vendor Certificates<br>Expiring in the Next 6 Months",
                yaxis=dict(title="Number of Certificates"),
                xaxis=dict(title="Month-Year"),
                font=dict(family="Arial, sans-serif", size=14, color="black")
            )
        }),
    ], style={'width': '49%', 'display': 'inline-block', 'height': '500px'}),
    
    html.Div([
        dcc.Dropdown(id='company-dropdown', options=[{'label': alias, 'value': alias} for alias in df_c2['Alias'].unique()],
                     multi=True, placeholder='Select company...'),
        dcc.Graph(id='c2-chart'),
        dcc.RangeSlider(
            id='year-slider',
            min=df_c2['Year'].min(),
            max=df_c2['Year'].max(),
            value=[df_c2['Year'].min(), df_c2['Year'].max()],
            marks={int(year): str(int(year)) for year in sorted(df_c2['Year'].unique())},
            step=1
        )
    ], style={'width': '49%', 'display': 'inline-block', 'vertical-align': 'top', 'height': '500px'}),

    html.Div([
        dcc.Graph(id='c3-chart', figure={
            'data': [
                go.Scatter(x=df_c3['Years'], y=df_c3['Registered'], mode='lines+markers', name='Registered', line=dict(width=4)),
                go.Scatter(x=df_c3['Years'], y=df_c3['Has Valid Certificate'], mode='lines+markers', name='Has Valid Certificate', line=dict(width=4))
            ],
            'layout': go.Layout(
                title='Number of Vendors in Five Years',
                xaxis=dict(title='Year'),
                yaxis=dict(title='Number of Vendors'),
                hovermode='x unified',
                font=dict(family="Arial, sans-serif", size=14, color="black"),
                #legend=dict(orientation="h",yanchor="bottom", y=1.02,xanchor="right",x=1)
                ),

                
            
        }),
    ], style={'width': '49%', 'display': 'inline-block', 'height': '500px', 'marginTop': '20px'}),

  html.Div(id='hover-data', style={'fontSize': 20, 'border': '1px solid black', 'padding': '10px', 'width': '22%', 'display': 'inline-block', 'vertical-align': 'text-bottom'})
    
])

@callback(
    Output('c1-chart', 'figure'),
    [Input('c1-chart', 'id')]  # This input is just a placeholder to trigger the callback when the app starts.
)
def update_c1_chart(_):
    # Create the bar chart
    fig_c1 = go.Figure()
    fig_c1.add_trace(go.Bar(x=certificate_counts.index, y=certificate_counts.values, marker_color='RoyalBlue'))
    
    # Add annotations
    for month, count in certificate_counts.items():
        fig_c1.add_annotation(
            x=month,
            y=count,
            text=str(count),
            showarrow=True,
            arrowhead=7,
            ax=0,
            ay=-20
        )
    
    # Update layout
    fig_c1.update_layout(
        title="Number of Vendor Certificates<br>Expiring in the Next 6 Months",
        title_x=0.5,
        yaxis=dict(title="Number of Certificates"),
        xaxis=dict(title="Month-Year"),
        font=dict(family="Arial, sans-serif", size=14)
    )
    
    return fig_c1.to_dict()


@callback(
    Output('c2-chart', 'figure'),
    [Input('year-slider', 'value'),
     Input('company-dropdown', 'value')]
)
def update_c2_figure(selected_years, selected_companies):
    filtered_df = df_c2[(df_c2['Year'] >= selected_years[0]) & (df_c2['Year'] <= selected_years[1])]
    if selected_companies:
        filtered_df = filtered_df[filtered_df['Alias'].isin(selected_companies)]
    fig_c2 = go.Figure()
    fig_c2.add_trace(go.Bar(y=filtered_df['Alias'], x=filtered_df['Number of Black Sanction'], name='Black Sanction', orientation='h', marker_color='#e28743'))
    fig_c2.add_trace(go.Bar(y=filtered_df['Alias'], x=filtered_df['Number of Red Sanctions'], name='Red Sanction', orientation='h', marker_color='#5ea1c3'))
    fig_c2.add_trace(go.Bar(y=filtered_df['Alias'], x=filtered_df['Number of Yellow Sanctions'], name='Yellow Sanction', orientation='h', marker_color='#a3c9dd'))
    fig_c2.update_layout(barmode='stack', title='Vendors who received the most sanctions', yaxis_title='Vendor Name', xaxis_title='Number of Sanction',
                         yaxis=dict(autorange="reversed"), font=dict(family="Arial, sans-serif", size=14, color="black"))
    return fig_c2

@callback(
    Output('hover-data', 'children'),
    [Input('c3-chart', 'hoverData')]
)
def update_hover_info(hoverData):
    if hoverData:
        year = hoverData['points'][0]['x']
        hover_info = [html.Div(f"Year: {year}", style={'fontSize': '20px', 'fontWeight': 'bold'})]
        for point in hoverData['points']:
            if point['y'] != 0:
                trace_name = point['curveNumber']
                value = point['y']
                if trace_name == 0:
                    hover_info.append(html.Div(f"Registered Vendors: {value}", style={'fontSize': '16px'}))
                elif trace_name == 1:
                    hover_info.append(html.Div(f"Vendors with Valid Certificate: {value}", style={'fontSize': '16px'}))
        return hover_info
    return html.Div("Hover over the graph!", style={'fontSize': '16px'})
