from flask_wtf import FlaskForm
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class SurveyForm(FlaskForm):
    register = BooleanField('I would like to register in this course',
                            validators=[DataRequired()])
    submit = SubmitField('Register')
