from flask.ext.wtf import Form, TextField, BooleanField, PasswordField, Email, ValidationError
from flask.ext.wtf import Required, EqualTo, RecaptchaField
import db


def validate_user(form, field):
    if (db.user_exists(field.data)):
        raise ValidationError("This username is already in use!")

def validate_email(form, field):
    if (db.email_exists(field.data)):
        raise ValidationError("This email is already in use!")

class LoginForm(Form):
    username = TextField('username', validators = [Required()])
    password = PasswordField('password', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)

class RegisterForm(Form):
    username = TextField('Username', validators = [Required(), validate_user])
    password = PasswordField('Password', validators = [Required(), EqualTo('password_conf', message="Passwords Must Match.")])
    password_conf = PasswordField('Repeat Password')
    email = TextField('Email', validators = [Email("Not a valid email address."), validate_email])
    name = TextField('Name (Optional)')
    city = TextField('City (Optional)')
    recaptcha = RecaptchaField()
