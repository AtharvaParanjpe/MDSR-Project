# MDSR-Project

## App.py
This file is the container of the server application which is used to render the templates found under the template directory.
Our main template is ourPage.html which is conditionally rendering the input and outputs based on the click of the button. 

## Graphpeel.py 
Includes our pyspark code which we used to run graph peeling using batching of the data.
In this we follows our algorithmic logic <br/>
Given a graph G and peeling value k, 

    - Remove vertices of degree less than or equal to k from G
    - If there are vertices left, G = G - the edges of the removed vertices
    - Repeat from step 1 until there are no vertices of degree less than k remaining
We have outputted the number of nodes removed at every iteration and have modularized every function to be easily integrable in case of future extension.

## Test.txt
This is a sample file we used for generating the graphs and obtaining the results as well as for the live demo.

## Misc. Resources
The resources for the background image and the css can be obtained under the 'static/styles' folder which follows the flask file convention.

## Running the code
You can run the code by: 
- clone the repository
- pip install flask, plotly, networkx
- run :  python app.py in terminal in the folder of the repository
- webapp runs at : localhost:8080/Peeling
