from flask import Flask, render_template
import matplotlib.pyplot as plt
import io
import base64
import numpy as np

# Importe Dash e componentes necessários
import dash
from dash import html, dcc, Input, Output
from dash.dcc import Dropdown, Graph
import dash_bootstrap_components as dbc
from support_2 import MyPlots  # Suponha que MyPlots seja um módulo personalizado
import pandas as pd
import plotly.graph_objects as go

# Criação do objeto Dash
external_stylesheets = [dbc.themes.BOOTSTRAP]
app_dash = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app_dash.title = "AFC Geofísica - Dashboard"

# Definição da classe Home
class Home:
    def __init__(self, server):
        self.app = dash.Dash(__name__, server=server, url_base_pathname='/dash/')
        self.app.title = "AFC Geofísica - Dashboard"
        self.set_data(MyPlots())  # Supondo que MyPlots seja uma classe que você definiu
        self.layout = self.draw()

    def set_data(self, myplots):
        self.myplots = myplots

    def draw(self):
        fig = go.Figure(go.Scatter(x=pd.Series(dtype=object), y=pd.Series(dtype=object), mode="markers"))

        header = html.Div(
            [
                dbc.Row([
                        dbc.Col(dbc.CardImg(src="/assets/AFC logo 1x1.jpg", class_name ="img-thumbnail img-fluid w-auto h-auto m-0 p-0"),
                                width=2,
                                style={"width": "130px"},
                                class_name=""),
                        dbc.Col(html.P(children='Delfos Viewer', className="", id='title'),
                            width=6,
                            class_name ="h1 text-start m-auto ms-0"),
                        dbc.Col(
                            html.Div(
                                [
                                    dbc.Button(
                                        [
                                            html.I(className="fas fa-star"),
                                            "Sair",
                                        ],
                                        id="logout-button",
                                        color="primary",
                                        className="text-right",
                                        href="/logout",
                                        style={"width": "50px;","float": "right"}
                                    ),
                                    html.P(
                                        "Olá " + "Usuário" + "! ",  # Aqui pode ser seu nome de usuário
                                        style={"float": "right", "padding-right":"10px" }
                                    ),
                                ],
                                className="text-right",
                            ),
                            width=3,
                            class_name="text-right",
                        ),
                    ],
                    class_name ="m-2 h-auto",
                ),
            ]
        )

        items = ["L1","L2", "L3", "L4"]

        selector = html.Div(
            dbc.Row([
                dbc.Col(dbc.Label("Linha:", class_name = ""),
                        width = 1,
                        style={"width": "60px"},
                        class_name = "mt-auto"
                        ),
                dbc.Col(dcc.Dropdown(items, "L1", className="w-90", id='selector_line', searchable=False,),
                        width = 1,
                    ),
                dbc.Col(dbc.Label("Dados recentes:"),
                        width = 1,
                        style={"width": "88px"},
                        class_name = "mt-auto border-start"
                        ),
                dbc.Col(dcc.Dropdown(items, className="w-90", id='selector_dados1', searchable=False,),
                        width = 2,
                    ),
                dbc.Col(dbc.Label("Dados antigos:"),
                        width = 1,
                        style={"width": "88px"},
                        class_name = "mt-auto border-start"
                        ),
                dbc.Col(dcc.Dropdown(items, className="w-90", id='selector_dados2', searchable=False,),
                        width = 2,
                    ),
                ], class_name ="m-2 h-auto",
                )
            )

        plots = dbc.Row([
            dbc.Col(dcc.Graph(figure=fig, id='fig2', className="", style={"height": "300px"}),
                    width=6,
                    class_name=""),
            dbc.Col(dcc.Graph(figure=fig, id='fig1', className="", style={"height": "100%"}),
                    width=6,
                    class_name =""),
            ],
            className ="m-2",
            )

        plots1 = dbc.Row([
            dbc.Col(dcc.Graph(figure=fig, id='figDiff', className="", style={"height": "300px"}),
                    width=6,
                    class_name=""),
            dbc.Col(dcc.Graph(figure=fig, id='figAvg', className="", style={"height": "100%"}),
                    width=6,
                    class_name =""),
            ],
            class_name ="m-2",
            )

        slider = dbc.Row([
            dbc.Col(dcc.RangeSlider(0, 1, value=[0, 1], id='sliderDiff'),
            width = 6,
            class_name = "m-2")
        ])

        graficos = html.Div([plots, plots1, slider])

        tab_voxel = html.Div([
            dbc.Row([
                dbc.Col(dbc.Label("Opacidade:", class_name = ""), width = 1, style={"width": "80px"}, class_name = "mt-auto"),
                dbc.Col(dcc.Slider(min = 0, max = 10, step = 1, value = 4, id = 'opacitySlider'), width=3),
            ], class_name = 'm-3'),
            dcc.Graph(figure = fig, id= 'figVoxel', style={"height": "800px"})
        ])

        tab_slice = html.Div([
            dbc.Row([
                dbc.Col(dbc.Label("Camada:", class_name = ""), width = 1, style={"width": "80px"}, class_name = "mt-auto"),
                dbc.Col(dcc.Slider(min = 0, max = 10, step = 1, value = 4, marks= {2: '10'}, id = 'selector_slice', included=False), width=4),
                dbc.Col(dbc.Label("Escala:", class_name = ""), width = 1, style={"width": "80px"}, class_name = "mt-auto"),
                dbc.Col(dcc.RangeSlider(0, 1, value=[0, 1], id='sliderLayer'), width = 5, class_name = "mt-auto ms-3")
            ], class_name = 'm-3'),
            dcc.Graph(figure = fig, id= 'figLayer', style={"height": "500px"})
        ])

        tabs = dcc.Tabs([
            dcc.Tab(label = 'Seções', children= graficos),
            dcc.Tab(label= 'Voxel', children = tab_voxel),
            dcc.Tab(label= 'cortes', children = tab_slice)
        ])

        layout = html.Div([header, selector, tabs])
        return layout

    def slider_options(self, options):
        out = {}
        for x in range(len(options)):
            out[x] = f'{options[x]}'
        return out

    def register_callbacks(self):
        @self.app.callback(
            Output("figLayer", "figure"),
            Input("sliderLayer", "value"),
            Input("selector_slice", "value"),
        )
        def set_layer_figure(slider, layer):
            figg = go.Figure()
            if (self.myplots.data2 is not None) and (self.myplots.data1 is not None):
                contours = dict(start = slider[0], end = slider[1], showlines= True)
                figg, minn, maxx = self.myplots.return_slice(layer, cont= contours)
            return figg

        @self.app.callback(
            [
                Output("sliderLayer", "min"),
                Output("sliderLayer", "max"),
                Output("sliderLayer", "value"),
            ],
            Input("selector_slice", "value")
        )
        def selector_slice(layer):
            minn = 0
            maxx = 1
            if (self.myplots.data2 is not None) and (self.myplots.data1 is not None):
                figg, minn, maxx = self.myplots.return_slice(layer)
            return round(minn,1), round(maxx,1), [minn, maxx]

        @self.app.callback(
            [
                Output("selector_dados1", "options"),
                Output("selector_dados2", "options")
            ],
            Input("selector_line", "value"),
        )
        def line_selected(line):
            self.myplots.clean_data()
            self.myplots.files_data = self.myplots.files_data_complete[self.myplots.files_data_complete['file'].str.contains(line)]
            self.myplots.options = [x.split('/')[-1] for x in self.myplots.files_data['file']]
            saida = self.myplots.files_data[self.myplots.files_data['file'].str.contains(line)]['data'].to_list()
            return saida, saida

        @self.app.callback(
            Output("figDiff", "figure"),
            Input('sliderDiff', 'value')
        )
        def set_avg(values):
            if (self.myplots.data2 is not None) and (self.myplots.data1 is not None):
                diff_data = self.myplots.data[self.myplots.data["diff"].notnull()]
                X, Y, grid_x, grid_y, data = self.myplots.to_grid((diff_data["x"],diff_data["y"]), diff_data["diff"])
                contour = dict(start = values[0], end = values[1], size = None, showlines= True)
                figg = self.myplots.return_contour_generic(data, X, Y, title='Diferença', cont = contour)
                return figg
            else:
                return go.Figure()

        @self.app.callback(
            Output("figVoxel", "figure"),
            Input("opacitySlider", "value")
        )
        def return_voxel(opacity):
            figg = go.Figure()
            if (self.myplots.data2 is not None) and (self.myplots.data1 is not None):
                figg = self.myplots.return_volume(self.myplots.complete_list(), opacity=opacity/10)
            return figg

        @self.app.callback(
            [
                Output("fig1", "figure"),
                Output("fig2", "figure"),
                Output("figAvg", "figure"),
                Output("selector_slice", "max"),
                Output("selector_slice", "marks"),
                Output("sliderDiff", "max"),
                Output("sliderDiff", "min"),
                Output("sliderDiff", "value"),
                Output('opacitySlider', 'value')
            ],
            [
                Input("selector_dados1", "value"),
                Input("selector_dados2", "value"),
            ]
        )
        def set_figures(file1, file2):
            fig1 = go.Figure()
            fig2 = go.Figure()
            figDiff = go.Figure()
            figAvg = go.Figure()
            marks = None
            max_slider = 3
            diffMax = 1
            diffMin = 0
            if file1:
                file1 = self.myplots.files_data[self.myplots.files_data['data'].str.contains(file1)]['file'].iloc[0].split('/')[-1]
                self.myplots.set_data1(file1)
                marks = self.slider_options(self.myplots.Y)
                max_slider = len(self.myplots.Y) - 1
            if file2:
                file2 = self.myplots.files_data[self.myplots.files_data['data'].str.contains(file2)]['file'].iloc[0].split('/')[-1]
                self.myplots.set_data2(file2)
                marks = self.slider_options(self.myplots.Y)
                max_slider = len(self.myplots.Y) - 1
            if self.myplots.data1 is not None:
                fig1 = self.myplots.return_contour(self.myplots.data1, cont=self.myplots.contours, log=True, title=self.myplots.date1)
            if self.myplots.data2 is not None:
                fig2 = self.myplots.return_contour(self.myplots.data2, cont=self.myplots.contours, log=True, title=self.myplots.date2)
            if (self.myplots.data2 is not None) and (self.myplots.data1 is not None):
                try:
                    diff = self.myplots.data["diff"]
                    diffMax = round(np.nanmax(diff), 1)
                    diffMin = round(np.nanmin(diff), 1)
                    figAvg = self.myplots.slice_avg()
                except:
                    pass
            return fig1, fig2, figAvg, max_slider, marks, diffMax, diffMin, [diffMin, diffMax], 5

# Criação do servidor Flask
app_flask = Flask(__name__)
server = app_flask

# Criação de uma instância de Home
home = Home(server)
home.register_callbacks()

# Rota para renderizar a página principal
@app_flask.route('/')
def index():
    return render_template('index.html', content=home.layout)

# Rota para o Dash
app_dash.layout = home.layout
app_dash.title = 'Dash Integration'
app_dash.config.suppress_callback_exceptions = True

# Rota para o Dash
@app_flask.route('/dash/')
def dash_app():
    return app_dash.index()

if __name__ == '__main__':
    app_flask.run(debug=True)