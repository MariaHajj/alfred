import os
from flask_admin.contrib.sqla import ModelView
from flask_admin.model import typefmt
from functools import wraps
from datetime import date, datetime
from flaskthreads import AppContextThread

from flask_login import current_user

from alfred.core.home.views import main
from alfred.models import Major
from alfred.models import User
from flask_mail import Message
from alfred import mail
from flask import current_app, send_file, redirect, app
import os.path as op

from flask import flash, Markup, url_for, send_from_directory

# Show null values instead of empty strings.
MY_DEFAULT_FORMATTERS = dict(typefmt.BASE_FORMATTERS)
MY_DEFAULT_FORMATTERS.update({type(None): typefmt.null_formatter})


class UserView(ModelView):
    form_columns = (
        'aub_id',
        'email',
        'first_name',
        'last_name',
        'password',
        'role',
        'major'
    )
    column_sortable_list = ('first_name', ('major', 'major.id', 'id'))
    column_searchable_list = ('aub_id', 'email', 'first_name',
                              'last_name', Major.code)
    column_filters = ('aub_id', 'major')
    column_type_formatters = MY_DEFAULT_FORMATTERS


class RoleView(ModelView):
    pass


def date_format(view, value):
    return value.strftime('%Y-%m-%d, %H:%M')


MY_DEFAULT_FORMATTERS.update({
    type(None): typefmt.null_formatter,
    date: date_format
    })


class AnnouncementView(ModelView):
    column_exclude_list = ['user']
    form_excluded_columns = ['user', 'upload_date']
    column_default_sort = ('upload_date', True)
    column_type_formatters = MY_DEFAULT_FORMATTERS

    def after_model_change(self, form, model, is_created):
        form.upload_date = datetime.now()
        users = User.query.all()
        with current_app.app_context():
            for user in users:
                msg = Message("New Announcement",
                              sender=os.environ['MAIL_USERNAME'],
                              recipients=[user.email])

                msg.body = "New Announcement has been posted"
                thread = AppContextThread(target=send_async_email, args=[msg])
                thread.start()


def send_async_email(msg):
    with current_app.app_context():
        mail.send(msg)


class FacultyView(ModelView):
    pass


class DepartmentView(ModelView):
    pass


class MajorView(ModelView):
    pass


class CourseView(ModelView):
    form_excluded_columns = ['capacity_survey','petition', 'course_grade', 'course_availability']


class CourseAvailabilityView(ModelView):
    pass


class AvailabilityView(ModelView):
    pass


class FrequencyView(ModelView):
    pass


class TermView(ModelView):
    pass


class CourseGradeView(ModelView):
    pass


class CapacitySurveyView(ModelView):
    form_excluded_columns = ['number_of_requests', 'course', 'students']
    column_exclude_list = ['course', 'students']


class StudentsRegisteredInSurveysView(ModelView):
    pass


def special_requirement(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        try:
            # the admin(stored as env variable) is the only one who can see the transcripts
            if current_user.email == os.environ['MAIL_USERNAME']:
                return f(*args, **kwargs)
            else:
                return redirect(url_for('main.home'))
        except:
            return redirect(url_for('main.home'))

    return wrap


class PetitionView(ModelView):
    form_excluded_columns = ['date_decided']
    column_default_sort = ('date_submitted',True)
    column_type_formatters = MY_DEFAULT_FORMATTERS

    @main.route('/static/transcripts/<path:filename>')
    @special_requirement
    def transcript(filename):
        return send_from_directory("static",filename="transcripts/"+filename)

    def _user_formatter(view, context, model, name):
        if model.transcript:
            file_words = model.transcript.split("/")
            file_name = file_words[len(file_words)-1]
            markupstring = "<a href='%s'>%s</a>" %("/static/"+file_name, "transcript")

            return Markup(markupstring)
        else:
            return ""

    column_formatters = {
        'transcript': _user_formatter
    }

    def after_model_change(self, form, model, is_created):
        with current_app.app_context():
            msg = Message("Final Decision",
                          sender=os.environ['MAIL_USERNAME'],
                          recipients=[model.user.email])

            msg.body = "A final decision has been taken in regard to your request."
            thread = AppContextThread(target=send_async_email, args=[msg])
            thread.start()
    def on_model_change(self,form, model, is_created):
        model.date_decided = date.today()


class PetitionStatusView(ModelView):
    form_excluded_columns =['petition']


class PetitionTypeView(ModelView):
    form_excluded_columns = ['petition']