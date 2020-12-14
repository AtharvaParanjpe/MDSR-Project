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
    weightOfPath = TextField('Weight of Path')
    numNodes = TextField('Number of nodes in path')
    executionTime = TextField('Execution Time in seconds')

@app.route('/Peeling', methods =['GET', 'POST'])
def computeShortestPath():
    form = Form()   
    if request.method == 'POST':
        # print('Dataset choice:' + str(request.form["Datasets"]), file=sys.stderr)
        # print('Peel Value:' + str( form.kValue.data), file=sys.stdout)
        if form.validate() == False:
            return render_template('ourPage.html', form = form)
        else:
            kValue = form.kValue.data
            ## Enter stuff here






            return render_template('populatedPage.html', kValue = kValue)
    elif request.method == 'GET':
        return render_template('ourPage.html', form = form)
    


if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = '8080')
