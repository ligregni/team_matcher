from flask.ext.wtf import Form
from wtforms import IntegerField
from wtforms.validators import DataRequired

class InputForm(Form):
    number_of_teams = IntegerField('number_of_teams', validators=[DataRequired()])
