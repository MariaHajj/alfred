from flask import Blueprint, flash
from flask import render_template
from alfred.models import CapacitySurvey
from alfred import db
from flask_login import login_required
from alfred.core.surveys.forms import SurveyForm

surveys = Blueprint('surveys', __name__)


@surveys.route("/survey_register/<int:id>", methods=['GET', 'POST'])
@login_required
def survey_register(id):
    form =SurveyForm()
    survey = CapacitySurvey.query.get_or_404(id)
    if form.validate_on_submit():
        survey.number_of_requests += 1
        db.session.commit()
        flash('The form has been submitted successfully!', 'success')
    return render_template('surveys.html', survey=survey, form=form )