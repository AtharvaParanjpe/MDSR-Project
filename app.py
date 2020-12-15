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
            # listOfList = graphPeel.do_peeling(kValue, request.form["Datasets"], sc, spark)
            return render_template('ourPage.html', form=form, kValue = kValue, listOfList = listOfList)
    elif request.method == 'GET':
        return render_template('ourPage.html', form = form)

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = '8080')
