from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, PasswordField, RadioField, SelectField 
from wtforms.validators import ValidationError, DataRequired, EqualTo, Email
from flask.ext.wtf.recaptcha import RecaptchaField
#from flask.ext.wtf.html5 import NumberInput, IntegerRangeField
from models import User_db
import extras



def validate_user(form, field):
    user_checker = User_db()
    if (user_checker.username_exists(field.data)):
        raise ValidationError("This username is already in use!")

def validate_email(form, field):
    email_checker = User_db()
    if (email_checker.email_exists(field.data)):
        raise ValidationError("This email is already in use!")

class LoginForm(Form):
    username = TextField('username', validators = [DataRequired()])
    password = PasswordField('password', validators = [DataRequired()])
    remember_me = BooleanField('remember_me', default = False)

class RegisterForm(Form):
    username = TextField('Username', validators = [DataRequired(), validate_user])
    password = PasswordField('Password', validators = [DataRequired(), EqualTo('password_conf', message="Passwords Must Match.")])
    password_conf = PasswordField('Repeat Password')
    email = TextField('Email', validators = [Email("Not a valid email address."), validate_email])
    name = TextField('Name (Optional)')
    city = TextField('City (Optional)')
    recaptcha = RecaptchaField()

class WhereForm(Form):
    #assert html5.RangeInput()(self.expected_users, min=0, max=20000)
    address = TextField('Address')
    address2 = TextField('Address 2')
    city = TextField('City')
    state = SelectField('State:', choices=extras.states)
    zip = TextField('ZIP Code:')

class WhereFormLite(Form):
    addr = TextField('Address', validators = [DataRequired()])

class WhatForm(Form):
    dummy = TextField('DUMMY')
    
