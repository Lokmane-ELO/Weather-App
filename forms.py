from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField , BooleanField
from wtforms.validators import DataRequired, Length, EqualTo



class RegisterForm(FlaskForm):
    """Registration form."""
    username = StringField('Username', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField('Password again',
                                   validators=[DataRequired(), EqualTo('password')])
    accept_tos = BooleanField('I promise to behave!', [DataRequired()])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    """Login form."""
    username = StringField('Username', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('Password', validators=[DataRequired()])
    token = StringField('Token', validators=[DataRequired(), Length(6, 6)])
    submit = SubmitField('Login')