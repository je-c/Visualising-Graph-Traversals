import json

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

import plotly.graph_objects as go

from container import Container
from components import *

FONT_AWESOME = "https://use.fontawesome.com/releases/v5.7.2/css/all.css"
external_stylesheets = [dbc.themes.BOOTSTRAP, FONT_AWESOME]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
palette = {
    'yellow': '#f8e9a1',
    'red': '#f76c6c',
    'ltBlue': '#a8d0e6',
    'medBlue': '#374785',
    'drkBlue': '#24305e'
}

colours = {'background': '#f5fafc'} #palette['ltBlue']}
corner_fillet = 10

parameters_modal = parameters_modal()
graph_container = graph_container()


app.layout = html.Div(
    children=[
        dbc.Nav(
            [
                dbc.NavItem(
                    [
                        dbc.Button(
                            html.I(
                                className="fas fa-project-diagram", 
                                style = {'color': palette['drkBlue']}
                            ),
                            id='parameters-open',
                            className="ml-auto",
                            size = 'sm', 
                            style = {
                                'border': '0px',  
                                'background': 'rgb(0,0,0,0)', 'border': 'none'
                            }
                        ),
                        parameters_modal
                    ]
                ),

                dbc.NavItem(
                    [
                        dbc.Button(
                            html.I(
                                className="fas fa-question-circle", 
                                style = {'color': palette['drkBlue']}
                            ), 
                            id="popover-target",
                            size = 'sm',
                            style={
                                'border': '0px', 'right': 21.5, 
                                'background': 'rgb(0,0,0,0)', 'border': 'none'
                            }
                        ),

                        dbc.Popover(
                            [
                                dbc.PopoverHeader("Help"),
                                dbc.PopoverBody(
                                """
                                This network graph is, by default, produced randomly.
                                To specify computation parameters please find the controls 
                                menu in the top left of the window.
                                """
                                ),
                            ],
                            id="popover-help",
                            is_open=False,
                            target="popover-target",
                        ),
                    ]
                ),
            ]
        ),

        html.Div(
            [
                html.H1(
                    'Visualising Graph Traversal', 
                    style = {'text-align':'center'}
                )
            ]
        ),

        html.Div(
            [
                *graph_container
            ],
            id="app-modal"
        ),

        html.Div(
            [
                html.P(
                    dcc.Markdown(
                        """
                        The purpose of this app is to visualise the logic of various graph traversal algorithms.
                        Upon loading, the app produces an interactive representation of a __randomised__, __undirected__ 
                        graph with alphabetically named nodes. As this initial graph is randomised, simply refresh the page
                        to resolve any malformed or undesirable generations.
                        """
                    ),
                    style = {'text-align':'center'}
                ),

                html.P(
                    dcc.Markdown(
                        """
                        Currently, only simple implementations of Breadth First Search (BFS), Depth First Search (DFS),
                        Iterative Deepening Search (IDS), Dijkstra's Algorithm, and A* Search are implemented. These algorithms can
                        be selected from the *parameters menu in the top-left corner* of the page. Additional options for custom graph 
                        construction will be implemented in future updates.
                        """
                    ),
                    style = {'text-align':'center'}
                ),

                html.P(
                    dcc.Markdown(
                        """
                        Source code for this project, and other similar projects can be found on my [GitHub](https://github.com/je-c) 
                        profile. For any issues, bugs or feature requests, please do not hesitate to contact me at Jeremy.crow95@gmail.com
                        """
                    ),
                    style = {'text-align':'center'}
                )
            ],
            style={
                'backgroundColor': palette['ltBlue'], 
                'margin-right': '15px',
                'margin-left': '15px',
                'margin-top': '35px',
                'border-radius': str(corner_fillet) + 'px',
                'border': '0px',
                'box-shadow': '0 0 15px #666',
                'overflow': 'hidden'    
            },
        ),
    ],
    style={'height': '100vh','backgroundColor': colours['background']}
)


#callback for params modal
@app.callback(
    Output("parameters-modal", "is_open"),
    [Input("parameters-open", "n_clicks"), Input("parameters-close", "n_clicks")],
    [State("parameters-modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2: return not is_open
    return is_open
    
#callback for the help tooltip window
@app.callback(
    Output("popover-help", "is_open"),
    [Input("popover-target", "n_clicks")],
    [State("popover-help", "is_open")],
)
def toggle_popover(n, is_open):
    if n: return not is_open
    return is_open


#callback for graph update based on parameters
@app.callback(Output(component_id = 'Network Graph', component_property = 'figure'),
             [Input(component_id = 'slct_search', component_property = 'value')])
def update_data(option_selected):
    print(option_selected)
    print(type(option_selected))

    global colours
    global data

    #Initialise the figure 
    network = Container()
    layout, edge_trace, node_trace = network.build()
    fig = go.Figure(layout = layout)

    #Plot all edge traces
    for trace in edge_trace:
        fig.add_trace(trace)

    #Plot all node traces
    fig.add_trace(node_trace)

    #Remove plot features and legend for a clean representation
    fig.update_layout(
        showlegend = False,
        autosize = False,
        margin = dict(
            t=0, r=0,
            b=0, l=0
        ),
        clickmode='event+select',
        paper_bgcolor = 'rgba(0,0,0,0)', # transparent background
        plot_bgcolor = 'rgba(0,0,0,0)'
    )
    fig.update_xaxes(showticklabels = False)
    fig.update_yaxes(showticklabels = False)

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)