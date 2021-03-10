from flask import Blueprint
from flask_restx import Api

from alfred.core.users.api import api as users
from alfred.core.majors.api import api as majors


blueprint = Blueprint('api', __name__)
api = Api(blueprint)

api.add_namespace(users)
api.add_namespace(majors)
