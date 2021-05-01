from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired

from wtforms import StringField, SubmitField
from wtforms import SelectField
from wtforms.validators import DataRequired


class PetitionForm(FlaskForm):
    transcript = FileField('Upload transcript (PDF only!)',
                           validators=[FileRequired(),
                                       FileAllowed(['pdf'])])
    request_comment = StringField('Request Description',
                                  validators=[DataRequired()])
    petition_type = SelectField('Petition Type', choices=[])
    course = SelectField('Course', choices=[])

    submit = SubmitField('Submit')
