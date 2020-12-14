from flask_wtf import FlaskForm
from wtforms import TextField, SubmitField, BooleanField

from wtforms import validators, ValidationError
from wtforms.validators import DataRequired

class Registro(FlaskForm):
    name = TextField('Source Node', [validators.Required('Start Node Required')])
    last_name = TextField('Destination Node', [validators.Required('Ending Node Required')])
    email = TextField('Email', [validators.Required('Email required'), validators.Email('Email not valid')])
    submit = SubmitField('Submit')
