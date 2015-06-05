from flask.ext.wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired


class SignUpForm(Form):
    name = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])


class StartGameForm(Form):
    player1 = StringField('player1')
    player2 = StringField('player2')
    player3 = StringField('player3')
    player4 = StringField('player4')
    player5 = StringField('player5')


class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)
