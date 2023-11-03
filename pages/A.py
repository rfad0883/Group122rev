import pandas as pd
import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
from datetime import date, datetime
import datetime 
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/A', name="Company Performance", external_stylesheets=[dbc.themes.BOOTSTRAP], order=2)

####################### LOAD DATASET #############################
df3 = pd.read_csv('B3.csv',delimiter=';')
df6 =pd.read_csv('B6A.csv',delimiter=";")
df7 = pd.read_csv('B7.csv',delimiter=';')

####################### PAGE LAYOUT #############################
#forB6
df6['Percentage_Workload']=df6['Daily_Workload']*100/df6['Daily_Workload'].sum()

dfg = df6.sort_values(by='Percentage_Workload',ascending=False)
dfg9 = dfg.head(9)

df_others = dfg.drop(dfg9.index)

total_remaining= df_others['Percentage_Workload'].sum()
combine_remaining= {'Oil_and_Gas_Company_Name':['Others'],
    'Verification_per_Month':[0],
    'Daily_Workload':[0],
    'Percentage_Workload': total_remaining}

combine_remaining_df = pd.DataFrame(combine_remaining)
combine_data = pd.concat([dfg9, combine_remaining_df])
#print('combine_data', combine_data)
dfsort = combine_data.sort_values(by='Percentage_Workload',ascending=True)

#forB1
dropdown_month1 = [option for option in sorted(df3['Month'].unique())]
df3['Month'] = pd.to_datetime(df3['Month'])
df3['format_date'] = df3['Month'].dt.strftime('%B %Y')
dropdown_format_date1 = [option for option in sorted(df3['format_date'].unique())]


#forB3
dropdown_company= [option for option in sorted(df3['Oil_and_Gas_Company_Name'].unique())]
dropdown_month = [option for option in sorted(df3['Month'].unique())]
df3['Month'] = pd.to_datetime(df3['Month'])
df3['format_date'] = df3['Month'].dt.strftime('%B %Y')
dropdown_format_date = [option for option in sorted(df3['format_date'].unique())]


#forB7
dropdown_year = [option for option in sorted(df7['Year'].unique())]

#Content
webtitle = html.Header('Centralized Integrated Vendor Database', style={'textAlign': 'center', 'fontSize': '24px', 'color': 'white', 'backgroundColor': 'black', 'padding': '10px'})


title = html.H1('A. OIL AND GAS COMPANY PERFORMANCE INSIGHT',  style={'color': 'blue', 'fontSize': 17,'textAlign': 'left'})

no1 = dbc.CardBody(
        [
            html.P('Average Registration', style={'color': 'black', 'fontSize': 14,'textAlign': 'center'}),
            html.H4(id='Registration', style={'color': 'RoyalBlue', 'fontSize': 70,'textAlign': 'center'}),
            html.P('days', style={'color': 'black', 'fontSize': 17,'textAlign': 'center'}),
        ])

no2 = dbc.CardBody(
        [
            html.P('Average Update Profile', style={'color': 'black', 'fontSize': 14,'textAlign': 'center'}),
            html.H4(id='Update_Profile', style={'color': 'orange', 'fontSize': 70,'textAlign': 'center'}),
            html.P('days', style={'color': 'black', 'fontSize': 17,'textAlign': 'center'}),
        ])

no3 = dbc.CardBody(
        [
            html.P('Average Certificate Issued', style={'color': 'black', 'fontSize': 14,'textAlign': 'center'}),
            html.H4(id='Certificate_Issue', style={'color': 'black', 'fontSize': 70,'textAlign': 'center'}),
            html.P('certificate', style={'color': 'black', 'fontSize': 17,'textAlign': 'center'}),
            
        ])

#cards
card0 = dbc.Card(webtitle, color ='black')

card1 =dbc.Card(no1, color="light")

card2 = dbc.Card(no2, color='light')

card3 = dbc.Card(no3,color= 'light')

#column
cards = [
    dbc.Col(card1, width=4),
    dbc.Col(card2, width=4),
    dbc.Col(card3, width=4)
]

inter = dbc.Col (dcc.Interval( id='interval-1-component',
        interval=86400000,  # Update once a day daity interval
        n_intervals=0))

dateassumption = datetime.datetime(2023, 9, 13)

title_b6 = html.H1('Percentage of current on-going workload',style = {"textAlign":"center","font-size":"20px"})

g_b6 = dcc.Graph(id="graph_B6")

text_b6 = html.P('Total 100%',style = {"textAlign":"right","font-size":"15px","color":"blue","padding-right":"100px"})

title_b3 = html.H1("Fulfillment of Service Level Agreement",style = {"textAlign":"center","font-size":"20px"})

title_b1a = html.H1("Average Verification ", style = {"textAlign":"center","font-size":"20px"})

currentdate = html.H1(f"Date: {dateassumption.strftime('%d-%m-%Y')}", style = {"textAlign":"start","font-size":"16px"}),

dd_b1_mo = dcc.Dropdown(options=dropdown_format_date1, value="September 2023",id='monthly_optionB1') #need recover
dd_b3_co = dcc.Dropdown(options=dropdown_company, value='Energy Source EP', id='oil_company', multi=True)

dd_b3_mo = dcc.Dropdown(options=dropdown_format_date, value='September 2023', id='monthly_option')#need recover

g_b3 = dcc.Graph(id="graph_B3")

title_b7 = html.H1('Correlation between Company Budget and Number of Procurement',style = {"textAlign":"center","font-size":"20px"})

dd_b7 = dcc.Dropdown(options=dropdown_year, value='2023',id='year_option')

g_b7 = dcc.Graph (id="graph_B7")

#layout
layout = dbc.Container ([
    dbc.Row ([
        #dbc.Row(card0, justify='center', align=''),
        #dbc.Row(html.Header('Centralized Integrated Vendor Database', style={'textAlign': 'center', 'fontSize': '24px', 'color': 'white', 'backgroundColor': 'black', 'padding': '10px'})),
        dbc.Row(inter)
    ]),
    dbc.Row (
        [
            dbc.Col(title, width={'size':5}),
            dbc.Col(currentdate,width={'size':2})
        ],
        justify="between"
    ),
    #dbc.Row (dbc.Col(dd_b1_mo, width={'size':3, "order":2})),
    dbc.Row(
        [
            dbc.Col(
                [
                    dbc.Row(html.Br()),#empty line  
                    dbc.Row(html.Br()),
                    dbc.Row(html.Br()),
                    dbc.Row(dd_b1_mo),
                    dbc.Row(html.Br()),
                    dbc.Row(
                        [
                            dbc.Col(card1, width=4, align="end"),
                            dbc.Col(card2, width=4, align="end"),
                            dbc.Col(card3, width=4, align="end"),
                        ]
                    ),
                    dbc.Row(html.Br()),
                    dbc.Row(title_b1a)
                    
                ]
            ),
            
            dbc.Col(
                [   
                    dbc.Row(title_b6),
                    dbc.Row(g_b6), 
                    dbc.Row(text_b6, justify='end')              
                ]
            ),


        ],    
        
    ),
    
    dbc.Row(
        [
            dbc.Col(title_b3, width=6),
            dbc.Col(title_b7, width=6),
        ]
    ),

    dbc.Row(
        [
            dbc.Col(dd_b3_co, width={'size':3, "order":1}),
            dbc.Col(dd_b3_mo, width={'size':3, "order":2}),
            dbc.Col(dd_b7, width={'size':3, "order":3, "offset":3}),
        ]
    ),

    dbc.Row(
        [
            dbc.Col(g_b3, width=6),
            dbc.Col(g_b7, width=6)
        ]
    ),
        

])
    
#callback for graph B6
@callback (Output('graph_B6','figure'),
    Input('interval-1-component', 'n_intervals'))

def update_graph_B6(n):
    fig = px.bar(data_frame = dfsort, x='Percentage_Workload', y='Oil_and_Gas_Company_Name',
        orientation = 'h', color_discrete_map={'Percentage_Workload':'blue'})#,barmode='group')
    fig.update_traces(texttemplate='%{x:.2f}%', textposition = 'outside', marker=dict(color="RoyalBlue"))
    fig.update_yaxes(title_text='Oil and Gas Company')
    fig.update_layout()
    return fig

#callback for forB1

@callback(
    Output('Registration','children'),
    Output('Update_Profile','children'),
    Output('Certificate_Issue','children'),
    Input('monthly_optionB1','value')
    )

def update_graph(monthly_option_B1):
    selection_month = [str(monthly_option_B1)]
    filtered_dfB1= df3[df3['Month'].isin(selection_month)]

    #for Registration
    average_registration = filtered_dfB1.groupby('Month')['Average_Registration_Time'].mean(numeric_only=True).reset_index()
    avg_registration = int(average_registration['Average_Registration_Time'])


    #for update profile
    average_update_profile = filtered_dfB1.groupby('Month')['Average_Update_Profile_Time'].mean(numeric_only=True).reset_index()
    avg_updateprofile = int(average_update_profile['Average_Update_Profile_Time'])
 
    #for Certificate_Issue

    average_certificate = filtered_dfB1.groupby('Month')['Number_of_Certificate_Issued'].mean(numeric_only=True).reset_index()
    avg_certificate = int(average_certificate['Number_of_Certificate_Issued'])


    box1 = avg_registration,
    box2 = avg_updateprofile,
    box3 = avg_certificate,
    return box1, box2, box3 #fig


#callback for graph B3
@callback(
    Output('graph_B3','figure'),
    Input('oil_company','value'),
    Input('monthly_option','value'))

def update_graph_B3(oil_company_name, monthly_option_list):
    selection_company = [str(company) for company in oil_company_name]
    selection_month = [str(monthly_option_list)]
    #print(selection_month)
    filtered_df = df3[(df3['Oil_and_Gas_Company_Name'].isin(selection_company))]
    filtered_df2= filtered_df[(filtered_df['Month'].isin(selection_month))]

    fig = px.bar(data_frame = filtered_df2, x =['Average_Registration_Time','Average_Update_Profile_Time'], y='Oil_and_Gas_Company_Name', orientation = 'h', color_discrete_map={'Average_Update_Profile_Time':'orange', 'Average_Registration_Time':'RoyalBlue'},barmode='group')
    fig.update_xaxes(title_text="Days")
    fig.update_yaxes(title_text="Oil and Gas Company Name")
    fig.update_layout(legend=dict(orientation="h",yanchor="bottom", y=1.02,xanchor="right",x=1))
    return fig
    
#callback for graph B7

@callback(
    Output('graph_B7','figure'),
    Input('year_option','value'))

def update_graph(year_option_value):
    selection_year =[float(year_option_value)]
    #print(selection_year)
    filtered_df7 = df7[(df7['Year'].isin(selection_year))]
    
    filtered_df77 = filtered_df7.sort_values(by='Yearly_Budget')
  

    fig = px.scatter(filtered_df77,x ="Yearly_Budget", y = 'Number_of_Tender')
    fig.update_traces(marker=dict(color="RoyalBlue")),

    #print(filtered_df7['Yearly_Budget'])
    #print(filtered_df7['Number_of_Tender'])
    fig.add_scatter(x=[filtered_df77['Yearly_Budget'].mean()],
                y=[filtered_df77['Number_of_Tender'].mean()],
                marker=dict(
                    color='orange',
                    size=10
                ),
               name='mean')
    
    fig.update_xaxes(title_text = 'Yearly Budget', categoryorder='array', categoryarray=sorted(filtered_df77['Yearly_Budget']))
    fig.update_yaxes(title_text = 'Number of Tender')
    fig.update_layout(legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
                          
    return fig
