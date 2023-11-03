import dash
from dash import html

dash.register_page(__name__, path='/', name="Introduction 😃",order=1)

####################### PAGE LAYOUT #############################
layout = html.Div(children=[
    html.Div(children=[
        html.H2("Welcome to Centralized Integrated Vendor Database"),
        "Centralized Integrated Vendor Database (CIVD) is an application for supply chain management in upstream oil and gas business in Indonesia, which is very beneficial to assesses and verifies vendors based on their administrative compliance, past performance, and financial capacity. This application is also useful to manage the supply chain performance of oil and gas company in Indonesia.",
        html.Br(),html.Br(),
        html.Div("Company Performance", style={"font-weight": "bold", 'fontSize': 20}),
	    html.Div("Visualizes insights for government oversight (SKK Migas) on oil and gas company performance"),
        html.Br(),
        html.Div("Vendor Performance", style={"font-weight": "bold", 'fontSize': 20}),
	    html.Div("Offers insights for oil and gas companies to review vendor administration and performance"),
	    html.Br(),
        html.Div("Map", style={"font-weight": "bold", 'fontSize': 20}),
	    html.Div("Offers insights for oil and gas companies to related to Vendor location and business size"),
	    html.Br(),
        html.Div("Procurement Insight", style={"font-weight": "bold", 'fontSize': 20}),
	    html.Div("Displays active procurement details, aiding vendors in document preparation and compliance with the regulation"),

    ]),

], className="bg-light p-2 m-2")
