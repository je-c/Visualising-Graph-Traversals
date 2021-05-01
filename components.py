import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

palette = {'yellow': '#f8e9a1',
           'red': '#f76c6c',
           'ltBlue': '#a8d0e6',
           'medBlue': '#374785',
           'drkBlue': '#24305e'}

colours = {'background': palette['ltBlue']}
corner_fillet = 10

def graph_container():
    return dcc.Graph(
        config = {
            'scrollZoom': True, 
            'responsive': True, 
            'displayModeBar': False
        },
        id='Network Graph',
        figure={}
    ),

def parameters_modal():
    return dbc.Modal(
        [
            dbc.ModalHeader("Modify graph parameters"),
            dbc.ModalBody(
                [
                    dcc.Dropdown(
                        id = 'slct_search',
                        options = [
                            {'label': 'BFS', 'value': 1},
                            {'label': 'DFS', 'value': 2},
                            {'label': 'IDS', 'value': 3},
                            {'label': 'Dijkstra', 'value': 4},
                            {'label': 'A*', 'value': 5}
                        ],
                        multi = False,
                        placeholder = 'Select a search algorithm'
                    ),
                ]
            ),

            dbc.ModalFooter(
                dbc.Button(
                    "Close", id="parameters-close", className="ml-auto"
                )
            ),
        ],
        id="parameters-modal",
        centered=True
    )
