from flask import Flask, render_template, request, flash
from flask_wtf import FlaskForm
import sys
import graphPeel
from wtforms import TextField, SubmitField, BooleanField

from wtforms import validators, ValidationError
from wtforms.validators import DataRequired

import findspark
findspark.init('/usr/local/Cellar/apache-spark/3.0.1/libexec')
import pyspark
from pyspark import SparkContext    
from pyspark.sql import SparkSession 

import numpy as np
import os
import time
from pyspark.sql.types import *
import time
import os 
import sys


import plotly.graph_objects as go
import json
import plotly

import networkx as nx



def generate_interactive_graph(G):
    pos_ = nx.spring_layout(G)

    def make_edge(x, y, text, width):
        return  go.Scatter(x         = x,
                        y         = y,
                        line      = dict(width = width,
                                    color = 'cornflowerblue'),
                        hoverinfo = 'text',
                        text      = ([text]),
                        mode      = 'lines')
    edge_trace = []
    for edge in G.edges():
        
        
        char_1 = edge[0]
        char_2 = edge[1]
        x0, y0 = pos_[char_1]
        x1, y1 = pos_[char_2]
        text   = str(char_1) + '--' + str(char_2) + ': ' + str(1)
        trace  = make_edge([x0, x1, None], [y0, y1, None], text, 
                            width = 0.3*1**1.75)
        edge_trace.append(trace)


    # Make a node trace
    node_trace = go.Scatter(x         = [],
                            y         = [],
                            text      = [],
                            textposition = "top center",
                            textfont_size = 10,
                            mode      = 'markers+text',
                            hoverinfo = 'none',
                            marker    = dict(color = [],
                                            size  = [],
                                            line  = None))
    # For each node in midsummer, get the position and size and add to the node_trace
    for node in G.nodes():
        x, y = pos_[node]
        node_trace['x'] += tuple([x])
        node_trace['y'] += tuple([y])
        node_trace['marker']['color'] += tuple(['cornflowerblue'])
        node_trace['marker']['size'] += tuple([5*3])
        node_trace['text'] += tuple(['<b>' + str(node) + '</b>'])

    # Customize layout
    layout = go.Layout(
        paper_bgcolor='rgba(0,0,0,0)', # transparent background
        plot_bgcolor='rgba(0,0,0,0)', # transparent 2nd background
        xaxis =  {'showgrid': False, 'zeroline': False}, # no gridlines
        yaxis = {'showgrid': False, 'zeroline': False}, # no gridlines
    )
    fig = go.Figure(layout = layout)
    for trace in edge_trace:
        fig.add_trace(trace)
    fig.add_trace(node_trace)
    fig.update_layout(showlegend = False)
    fig.update_xaxes(showticklabels = False)
    fig.update_yaxes(showticklabels = False)
    fig.show()

def create_interactive_graph(nodes, kValue):
    G = nx.random_geometric_graph(10, 0.125)

    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = G.nodes[edge[0]]['pos']
        x1, y1 = G.nodes[edge[1]]['pos']
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = G.nodes[node]['pos']
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))

    node_adjacencies = []
    node_text = []
    for node, adjacencies in enumerate(G.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))
        node_text.append('# of connections: '+str(len(adjacencies[1])))

    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text        
    fig = go.Figure(data=[edge_trace, node_trace],
                layout=go.Layout(
                    title='<br>Graph after peeling',
                    titlefont_size=16,
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                    annotations=[ dict(
                        text="Python code: <a href='https://plotly.com/ipython-notebooks/network-graphs/'> https://plotly.com/ipython-notebooks/network-graphs/</a>",
                        showarrow=False,
                        xref="paper", yref="paper",
                        x=0.005, y=-0.002 ) ],
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )
    fig.show()



sc = SparkContext('local')
spark = SparkSession(sc) 
app = Flask(__name__)
app.secret_key = 'development key'

class Form(FlaskForm):
    kValue = TextField('Peel Value', [validators.Required('Cannot be Empty!')])
    
@app.route('/Peeling', methods =['GET', 'POST'])
def computeShortestPath():
    form = Form() 
    
    if request.method == 'POST':
        if not ("kValue" in request.form) or not("Datasets" in request.form):
            return render_template('ourPage.html', form = form)
        else:
            kValue = request.form["kValue"]
            listOfList = [ [1,11232,1000], [2,11232,1000]]
            listOfList = graphPeel.do_peeling(kValue, request.form["Datasets"], sc, spark)
            print ("Before Graphtype ")
            Graphtype=nx.Graph()  
            print ("Before read_edgelist ")


            G = nx.read_edgelist(
                "graph_plot.txt", 
                create_using=Graphtype,
                nodetype=int,
            )
            print ("Before generate_interactive_graph ")
            graph = generate_interactive_graph(G)
            print ("After generate_interactive_graph ")
            return render_template('ourPage.html', form=form, kValue = kValue, listOfList = listOfList, graph = graph)
    elif request.method == 'GET':
        return render_template('ourPage.html', form = form)

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = '8080')
