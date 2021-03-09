from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed

from wtforms import StringField, PasswordField, SubmitField
from wtforms import BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms.validators import ValidationError, Required

from flask_login import current_user
from alfred.models import User


class RegistrationForm(FlaskForm):
    aub_id = StringField('AUB ID', validators=[Required(),
                                               Length(min=9, max=12)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    # major = StringField('Major', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    submit = SubmitField('Submit')

    def validate_aub_id(self, aub_id):
        user = User.query.filter_by(aub_id=aub_id.data).first()

        if user:
            raise ValidationError('AUB ID already exists!')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()

        if user:
            raise ValidationError('Account with email already exists!')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log in')


class UpdateAccountForm(FlaskForm):
    aub_id = StringField('AUB ID', validators=[DataRequired(),
                                               Length(min=9, max=12)])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    image = FileField('Update Profile Picture',
                      validators=[FileAllowed(['jpg', 'jpeg', 'png'])])

    submit = SubmitField('Update')

    def validate_aub_id(self, aub_id):
        if aub_id.data != current_user.aub_id:
            user = User.query.filter_by(aub_id=aub_id.data).first()
            if user:
                raise ValidationError('aub_id already taken!')

