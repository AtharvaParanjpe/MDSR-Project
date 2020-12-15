from flask import Flask, render_template, request, flash
from flask_wtf import FlaskForm
import sys
# import graphPeel
from wtforms import TextField, SubmitField, BooleanField

from wtforms import validators, ValidationError
from wtforms.validators import DataRequired

# import findspark
# findspark.init('/usr/local/Cellar/apache-spark/3.0.1/libexec')
# import pyspark
# from pyspark import SparkContext    
# from pyspark.sql import SparkSession 

import numpy as np
import os
import time
# from pyspark.sql.types import *
import time
import os 



import plotly.graph_objects as go
import json
import plotly

import networkx as nx


def create_interactive_graph(nodes, kValue):
    G = nx.random_geometric_graph(nodes, kValue/8)

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



# sc = SparkContext('local')
# spark = SparkSession(sc) 
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
            graph = create_interactive_graph(nodes, int(kValue))
            # listOfList = graphPeel.do_peeling(kValue, request.form["Datasets"], sc, spark)
            return render_template('ourPage.html', form=form, kValue = kValue, listOfList = listOfList, graph = graph)
    elif request.method == 'GET':
        return render_template('ourPage.html', form = form)

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = '8080')
