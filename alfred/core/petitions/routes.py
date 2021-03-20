from flask import Blueprint,render_template
from flask_login import login_required
from alfred.models import PetitionType
from alfred import db
petitions = Blueprint('petitions', __name__)

@petitions.route("/petitions_form/<int:id>", methods=['GET', 'POST'])
@login_required
def petitions_form(id):
    Petition_type = PetitionType.query.get_or_404(id)
    return render_template('petitions.html',Petition_type=Petition_type)

@petitions.route("/request_history")
@login_required
def request_history():
    return render_template('request_history.html')

@petitions.route("/petition_request_details")
@login_required
def petition_request_details():
    return render_template('petition_request_details.html')