from flask_wtf import Form
from flask_wtf.file import FileField
from wtforms import TextField, HiddenField, ValidationError, RadioField,\
    BooleanField, SubmitField, IntegerField, FormField, validators, SelectField, \
    StringField, PasswordField
from game_store_db import *

class GameForm(Form):
    #Text
    title = TextField('Title',[validators.required('Input Invalid')])

    def validate_title(form, field):
        new_title = field.data
        if any(new_title == title for title in game_titles()):
            raise ValidationError(f"A game with Title:\'{new_title}\' already exists!")

    rating = TextField('ESRB Rating',[validators.required('Input Invalid')])
    platform = TextField('Game Platform',[validators.required('Input Invalid')])
    dev = TextField('Developer',[validators.required('Input Invalid')])
    genre = TextField('Genre',[validators.required('Input Invalid')])

    #Numbers
    year = IntegerField('Year of Release', [validators.InputRequired('Please enter an integer')])
    price = IntegerField('Price', [validators.InputRequired('Please enter an integer')])

    submit_button = SubmitField('Add Title')

class SearchForm(Form):
    #Text
    title = TextField('Title',[validators.optional('Input Invalid')])
    rating = TextField('ESRB Rating',[validators.optional('Input Invalid')])
    platform = TextField('Game Platform',[validators.optional('Input Invalid')])
    dev = TextField('Developer',[validators.optional('Input Invalid')])
    #genre = TextField('Genre',[validators.optional('Input Invalid')])
    genre =  SelectField(u'Genre', coerce=str, choices=game_genres())

    #Numbers
    year = IntegerField('Year of Release', [validators.optional('Please enter an integer')])
    price = IntegerField('Price', [validators.optional('Please enter an integer')])

    submit_button = SubmitField('Search')

class ApplyFilter(Form):
    apply_filter = SubmitField('Apply Filter')

class ClearFilter(Form):
    clear_filter = SubmitField('Clear Filter')

class Checkout(Form):
    checkout = SubmitField('Checkout')

class Authenticate(Form):
    username = StringField('Username',[validators.required('Enter a Username')])
    password = PasswordField('Password',[validators.required('Enter a Username')])
    login = SubmitField('Sign In')
    register = SubmitField('Create Account')