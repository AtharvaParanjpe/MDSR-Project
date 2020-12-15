from flask import Flask, render_template, request, flash
from forms import *
from flask_wtf import FlaskForm
import sys
from wtforms import TextField, SubmitField, BooleanField

from wtforms import validators, ValidationError
from wtforms.validators import DataRequired

app = Flask(__name__)
app.secret_key = 'development key'

class Form(FlaskForm):
    kValue = TextField('Peel Value', [validators.Required('Cannot be Empty!')])
    # weightOfPath = TextField('Weight of Path')
    # numNodes = TextField('Number of nodes in path')
    # executionTime = TextField('Execution Time in seconds')

@app.route('/Peeling', methods =['GET', 'POST'])
def computeShortestPath():
    form = Form() 
    
    if request.method == 'POST':
        if not ("kValue" in request.form) or not("Datasets" in request.form):
            return render_template('ourPage.html', form = form)
        else:
            kValue = request.form["kValue"]
        ## Enter stuff here

            listOfList = [ [1,11232,1000], [2,11232,1000]]

            return render_template('ourPage.html', form=form, kValue = kValue, listOfList = listOfList)
    elif request.method == 'GET':
        return render_template('ourPage.html', form = form)
    


if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = '8080')
