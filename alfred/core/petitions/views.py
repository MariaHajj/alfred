from flask.globals import current_app
from alfred.core.petitions.api import api
from flask import Blueprint, request, jsonify
from flask import render_template, flash, redirect, url_for, abort
import requests
import json
from datetime import datetime, timezone
from alfred.dao.petition_types import petition_type_dao
from alfred.dao.petition_statuses import petition_status_dao
from alfred.dao.courses import course_dao
from alfred.dao.petitions import petition_dao
from alfred.dao.users import user_dao
from alfred.core.petitions.forms import PetitionForm
from flask_login import login_required, current_user
from alfred.utils import save_pdf
from alfred.services.petitions import petition_service
from alfred.models import Petition, PetitionType
from flask_mail import Message
from alfred import mail
from flaskthreads import AppContextThread
import os

petitions = Blueprint('petitions', __name__)


@petitions.route("/petition",
                 methods=['GET', 'POST'])
@login_required
def petition():

    form = PetitionForm()

    # to get all the courses for the drop down menu
    all_courses = requests.get('http://127.0.0.1:5000/api/1/courses/all')
    courses_data = json.loads(all_courses.text)
    choices = [i['name'] for i in courses_data['courses']]
    form.course.choices = choices

    # to get all the petition types for the drop down menu
    all_petition_types = requests\
        .get('http://127.0.0.1:5000/api/1/petition_types/all')
    types_data = json.loads(all_petition_types.text)
    choices = [i['name'] for i in types_data['types']]
    form.petition_type.choices = choices

    if form.validate_on_submit():
        with current_app.app_context():
                msg = Message("New Petition",
                              sender=os.environ['MAIL_USERNAME'],
                              recipients=[os.environ['MAIL_USERNAME']])

                msg.body = "new petition has been sent"
                thread = AppContextThread(target=send_async_email, args=[msg])
                thread.start()

        transcript_file = save_pdf(form.transcript.data)
        request_comment = form.request_comment.data
        date_submitted = datetime.utcnow()
        petition_type = petition_type_dao.get_by_name(form.petition_type.data)
        course = course_dao.get_by_name(form.course.data)
        petition_status = petition_status_dao\
            .get_by_name(name='Pending')
        advisor_comment = None
        decision_comment = None
        date_decided = None
        user = user_dao.get_by_email(current_user.email)

        petition_service.create_petition(transcript=transcript_file,
                                         request_comment=request_comment,
                                         date_submitted=date_submitted,
                                         petition_type=petition_type,
                                         course=course,
                                         petition_status=petition_status,
                                         advisor_comment=advisor_comment,
                                         decision_comment=decision_comment,
                                         date_decided=date_decided,
                                         user=user)

        flash('Petition submitted!', 'success')
        return redirect(url_for('main.home'))
    petition_type = PetitionType.query.all()
    return render_template('petitions.html',
                           title='petition',
                           form=form, petition_type=petition_type)


def send_async_email(msg):
    with current_app.app_context():
        mail.send(msg)
@petitions.route("/request_history")
@login_required
def request_history():

    request_history = petition_dao.get_by_user(current_user)

    return render_template('request_history.html',
                           title='history',
                           request_history=request_history)


@petitions.route("/petition_request_details/<int:petition_id>")
@login_required
def petition_request_details(petition_id):
    petition_details = Petition.query.filter_by(id=petition_id).first()
    if petition_details.user != current_user:
        abort(403)
    return render_template('petition_request_details.html',
                           title='details',
                           petition_details=petition_details)

@petitions.route('/description/<petition_type>')
def description(petition_type):
    petitions = PetitionType.query.filter_by(name=petition_type)

    petitionArray =[]
    for petition in petitions:
        petitionObj ={}
        petitionObj["description"] = petition.description
        petitionArray.append(petitionObj)

    return jsonify({'petition': petitionArray})




