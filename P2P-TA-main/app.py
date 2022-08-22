# -*- coding: utf-8 -*-
import numpy as np 
import pandas as pd 
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import dash_auth
import plotly.graph_objects as go
import plotly.figure_factory as ff
import matplotlib as plt
from pages import (Finland, overview)
from API import p2p_fig, user_names, fig_bar, p2p_trans_fig, text_full
import warnings
import dash_bootstrap_components as dbc
warnings.filterwarnings("ignore", category=FutureWarning)

app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])
app.title = "P2P trading algorithm"
server = app.server
app.config['suppress_callback_exceptions'] = True
# Describe the layout/ UI of the app

VALID_USERNAME_PASSWORD_PAIRS = {
    'Sender': '123'
}
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)

# Update page
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    #print(pathname)
    if pathname == "/dash-P2P-report/Austria":
        return Austria.create_layout(app)
    elif pathname == "/dash-P2P/Finland":
        return Finland.create_layout(app)
    elif pathname == "/dash-P2P/Spain":
        return Spain.create_layout(app)
    elif pathname == "/dash-P2P/overview":
        return overview.create_layout(app)
    #elif pathname == "/dash-financial-report/full-view":
        return (
            Austria.create_layout(app),
            Finland.create_layout(app),
            Spain.create_layout(app),
            overview.create_layout(app)
        )
    else:
        return overview.create_layout(app)


@app.callback(
    dash.dependencies.Output('dd-test-container', 'children'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_output(value):
    if value == "None":
        return "Select info"
    else: 
        return "{}".format(value)
@app.callback(
    dash.dependencies.Output('price', 'children'),
    [dash.dependencies.Input('priceinfo', 'value')])

def update_pinfo(value):
    return value

@app.callback(
    dash.dependencies.Output('priceb', 'children'),
    [dash.dependencies.Input('pricei', 'value')])

def update_pinfo(value):
    return value




#Dette er nytt
#%% Finland

@app.callback(
    Output('transfinland', 'figure'),
    Input('house', 'value'))

def update_fig_trans(house):
    
    fig=p2p_fig[house]
    
    return fig

@app.callback(
    Output('barfinland', 'figure'),
    Input('house', 'value'))

def update_fig_trans(house):
    
    #fig=p2p_fig[house]
    fig=fig_bar[house]
    
    return fig

@app.callback(
    Output('p2ptransfinland', 'figure'),
    Input('house', 'value'))

def update_fig_trans(house):
    
    #fig=p2p_fig[house]
    fig=p2p_trans_fig[house]
    
    return fig

#%%Austria

@app.callback(
    Output('transaustria', 'figure'),
    Input('house', 'value'))

def update_fig_trans(house):
    
    fig=p2p_fig[house]
    
    return fig

@app.callback(
    Output('baraustria', 'figure'),
    Input('house', 'value'))

def update_fig_trans(house):
    
    #fig=p2p_fig[house]
    fig=fig_bar[house]
    
    return fig

@app.callback(
    Output('p2ptransaustria', 'figure'),
    Input('house', 'value'))

def update_fig_trans(house):
    
    #fig=p2p_fig[house]
    fig=p2p_trans_fig[house]
    
    return fig

#%%Spain 

@app.callback(
    Output('transspain', 'figure'),
    Input('house', 'value'))

def update_fig_trans(house):
    
    fig=p2p_fig[house]
    
    return fig

@app.callback(
    Output('barspain', 'figure'),
    Input('house', 'value'))

def update_fig_trans(house):
    
    #fig=p2p_fig[house]
    fig=fig_bar[house]
    
    return fig

@app.callback(
    Output('p2ptransspain', 'figure'),
    Input('house', 'value'))

def update_fig_trans(house):
    
    #fig=p2p_fig[house]
    fig=p2p_trans_fig[house]
    
    return fig
    
    
if __name__ == "__main__":
    
    app.run_server(debug=True,host = '127.0.0.1')
    
    # serve(app.server, host="0.0.0.0", port=8050)
