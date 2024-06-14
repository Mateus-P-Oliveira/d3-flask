import dash
from dash import Dash, html, dcc, Input, Output
from dash.dcc import Dropdown, Graph
import dash_bootstrap_components as dbc
from flask import session
from support_2 import MyPlots
import numpy as np
import plotly.express as px
import pandas as pd

import plotly.graph_objects as go

class Home:
    def __init__(self, app):
        self.dashapp = dash.Dash(__name__)
        self.mainapp = app
        self.mainapp.title = "AFC Geofísica - Dashboard"

    def set_data(self, myplots):
        self.Myplots = myplots

    
    def draw(self):
        self.fig = go.Figure(go.Scatter(x=pd.Series(dtype=object), y=pd.Series(dtype=object), mode="markers"))

        plots = html.Div([
            dcc.Graph(figure=self.fig, id='fig2', className="", style={"height": "300px"}),
            dcc.Graph(figure=self.fig, id='fig1', className="", style={"height": "100%"}),
        ], className="m-2")

        plots1 = html.Div([
            dcc.Graph(figure=self.fig, id='figDiff', className="", style={"height": "300px"}),
            dcc.Graph(figure=self.fig, id='figAvg', className="", style={"height": "100%"}),
        ], class_name="m-2")

        slider = html.Div([
            dcc.RangeSlider(0, 1, value=[0, 1], id='sliderDiff'),
        ], class_name="m-2")

        graficos = html.Div([plots, plots1, slider])

        tab_voxel = html.Div([
            dcc.Slider(min=0, max=10, step=1, value=4, id='opacitySlider'),
            dcc.Graph(figure=self.fig, id='figVoxel', style={"height": "800px"})
        ])

        tab_slice = html.Div([
            dcc.Slider(min=0, max=10, step=1, value=4, marks={2: '10'}, id='selector_slice', included=False),
            dcc.RangeSlider(0, 1, value=[0, 1], id='sliderLayer'),
            dcc.Graph(figure=self.fig, id='figLayer', style={"height": "500px"})
        ])

        tabs = dcc.Tabs([
            dcc.Tab(label='Seções', children=graficos),
            dcc.Tab(label='Voxel', children=tab_voxel),
            dcc.Tab(label='cortes', children=tab_slice)
        ])

        self.dashapp.layout = html.Div([tabs])
        return self.dashapp.layout

    def run(self, debug=False):
        self.dashapp.run_server(debug=debug)
