from flask import Blueprint, flash
from flask import render_template,redirect,url_for
from alfred.models import CapacitySurvey,StudentsRegisteredInSurveys
from alfred import db
from flask_login import login_required,current_user
from alfred.core.surveys.forms import SurveyForm

surveys = Blueprint('surveys', __name__)


@surveys.route("/survey_register/<int:id>", methods=['GET', 'POST'])
@login_required
def survey_register(id):
    form =SurveyForm()
    student_submitted =False
    survey = CapacitySurvey.query.get_or_404(id)
    if StudentsRegisteredInSurveys.query.filter_by(survey_id=survey.id, student_id=current_user.id).first():
        student_submitted = True
    if form.validate_on_submit():
        survey.number_of_requests += 1
        register_student_in_survey=StudentsRegisteredInSurveys(survey_id=survey.id,student_id=current_user.id)
        db.session.add(register_student_in_survey)
        db.session.commit()
        flash('The form has been submitted successfully!', 'success')
        return redirect(url_for('main.home'))
    return render_template('surveys.html', survey=survey, form=form,student_submitted=student_submitted  )