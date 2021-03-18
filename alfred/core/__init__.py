from flask import Blueprint
from flask_restx import Api

from alfred.core.users.api import api as users
from alfred.core.majors.api import api as majors
from alfred.core.departments.api import api as departments
from alfred.core.faculties.api import api as faculties
from alfred.core.frequencies.api import api as frequencies
from alfred.core.terms.api import api as terms
from alfred.core.courses.api import api as courses
from alfred.core.capacity_surveys.api import api as capacity_surveys
from alfred.core.petition_statuses.api import api as petition_statuses
from alfred.core.petition_types.api import api as petition_types
from alfred.core.petitions.api import api as petitions
from alfred.core.announcements.api import api as announcement


blueprint = Blueprint('api', __name__)
api = Api(blueprint)

api.add_namespace(users)
api.add_namespace(majors)
api.add_namespace(departments)
api.add_namespace(faculties)
api.add_namespace(frequencies)
api.add_namespace(terms)
api.add_namespace(courses)
api.add_namespace(capacity_surveys)
api.add_namespace(petition_statuses)
api.add_namespace(petition_types)
api.add_namespace(petitions)
api.add_namespace(announcement)
