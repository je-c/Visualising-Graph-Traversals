from graph.run import InitialiseNetwork

import numpy as np
import pandas as pd
from datetime import datetime

import plotly.graph_objects as go
import networkx as nx

class Container(InitialiseNetwork):

    def __init__(self):
        super().__init__()
        self.nodes, self.edges = self.get_elements()

    def make_edge(self, x, y, text, width):
        return  go.Scatter(
            x=x, y=y,
            line=dict(
                width=width,
                color='black'
            ),
            hoverinfo='text',
            text=([text]),
            mode='lines'
        )

    def get_hover(self, node):
        return tuple(
            [
                f'<i>Degree: {self.net.degree[node]}</i>' +
                '<extra></extra>'
            ]
        )

    def build(self, method='Dij'):
        palette = {
            'yellow': '#f8e9a1',
            'red': '#f76c6c',
            'ltBlue': '#a8d0e6',
            'medBlue': '#374785',
            'drkBlue': '#24305e'
        }
        path_nodes = [i.name for i in self.find_path(self._vertices[0], self._vertices[-1])]
        #Initialise the networkx graph
        self.net = nx.Graph()

        #Define all nodes
        for node in self.nodes:
            if node in path_nodes:
                self.net.add_node(node, size = 1, tag='on')
            else:
                self.net.add_node(node, size = 1, tag='off')

        #Define all edges
        for _from in self.edges:
            for _to in self.edges[_from]:
                self.net.add_edge(
                    _from, _to, 
                    weight = 1
                )

        #Allocate a graphical position to each node
        pos_ = nx.spring_layout(self.net)

        textColour = 'black'
        traceColour = 'black'

        #Graphically define each edge
        edge_trace = []
        for edge in self.net.edges():
            entity = edge[0]
            supplier = edge[1]

            x0, y0 = pos_[entity]
            x1, y1 = pos_[supplier]

            text = entity + '--' + supplier + ': 1'

            trace = self.make_edge(
                [x0, x1, None], 
                [y0, y1, None],
                text,
                width = 1
            )
            
            edge_trace.append(trace)

        #Graphically define each node
        node_trace = go.Scatter(
            x=[], y=[],
            text=[], textposition="top center",
            textfont=dict(
                size=12,
                color='black'
            ),
            mode='markers+text',
            hovertemplate=[],
            marker=dict(
                color=[],
                opacity=[],
                size =[],
                line=dict(
                    color=[]
                )
            )
        )

        
        #For each node in the network, return graphical position and size and add to graph
        for node in self.net.nodes():
            x, y = pos_[node]
            node_trace['x']                         += tuple([x])
            node_trace['y']                         += tuple([y])
            node_trace['marker']['opacity']         += tuple([1])
            node_trace['marker']['color']           += tuple(['coral']) if self.net.nodes()[node]['tag'] == 'on' else tuple([palette['yellow']])
            node_trace['marker']['line']['color']   += tuple(['coral']) if self.net.nodes()[node]['tag'] == 'on' else tuple([palette['yellow']])
            node_trace['marker']['size']            += tuple([5+3*self.net.degree[node]])
            node_trace['text']                      += tuple(['<b>' + node + '</b>'])
            node_trace['hovertemplate']             += self.get_hover(node)

        #Layout customisation/parameters
        layout = go.Layout(
            paper_bgcolor='rgba(0,0,0,0)', # transparent background
            plot_bgcolor='rgba(0,0,0,0)', # transparent 2nd background
            xaxis={'showgrid': False, 'zeroline': False}, # no gridlines
            yaxis={'showgrid': False, 'zeroline': False}, # no gridlines
            dragmode='pan',
        )

        return layout, edge_trace, node_trace

        
        # #Initialise the figure
        # fig = go.Figure(layout = layout)

        # #Plot all edge traces
        # for trace in edge_trace:
        #     fig.add_trace(trace)

        # #Plot all node traces
        # fig.add_trace(node_trace)

        # #Remove plot features and legend for a clean representation
        # fig.update_layout(showlegend = False)
        # fig.update_xaxes(showticklabels = False)
        # fig.update_yaxes(showticklabels = False)

        # #Show the plot
        # fig.show(config = dict({'scrollZoom': True}))