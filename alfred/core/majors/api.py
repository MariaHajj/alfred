from alfred.schemas.majors import MajorSchema
from alfred.dao.majors import major_dao
from alfred.services.majors import major_service

from flask_restx import Namespace, Resource, reqparse


api = Namespace('majors', description='Major-related operations')
major_schema = MajorSchema()


@api.route('/all')
@api.response('200', 'Success')
class Majors(Resource):
    def get(self):
        """An endpoint to get all majors from the database.

        Parameters
        ----------
        None

        Returns
        -------
        [JSON]
            dict of the form {"majors": [list-of-majors]}
        """
        all_majors = major_dao.get_all()
        return major_schema.dump(all_majors, many=True)


parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('code', required=True)


@api.route('/add')
@api.response('201', 'Success: The major was created successfully.')
@api.response('400', 'Error: Bad request. Check parameters.')
@api.response('422', 'Error: The request failed.')
class AddMajor(Resource):
    """Resource to add a new major.
    """
    @api.expect(parser)
    def post(self):
        """Add a new major.

        Parameters
        ----------
        - name:
            major name has to be unique.
        - code:
            major's code has to be unique.
        """
        args = parser.parse_args()
        name = args['name']
        code = args['code']

        if name and code:
            try:
                major_service.create_major(name=name, code=code)
                return "The major was created successfully.", 201
            except Exception as e:
                api.abort(422, e, status="Could not save information",
                          statusCode="422")


@api.route('/<int:major_id>')
@api.param('major_id', 'Major identifier', required=True)
@api.response('200', 'Success: Major found.')
@api.response('404', 'Error: Major not found.')
class getMajor(Resource):
    """Resource to get a major by their ID.
    """
    def get(self, major_id):
        """Get major by id.

        Parameters
        ----------
        - major_id : [int]

        Returns
        -------
        [JSON]
            dict with the structure:
            {
                "major": {
                    "name": name,
                    "code": code,
                }
            }
        """
        major = major_dao.get_by_id(major_id=major_id)
        if major:
            return major_schema.dump(major)

        api.abort(404, message="The major was not found.",
                  status="Could not find information", statusCode="404")


@api.route('/<name>')
@api.param('name', required=True)
@api.response('200', 'Success: Major found.')
@api.response('404', 'Error: Major not found.')
class getMajorName(Resource):
    """Resource to get a major by their name.
    """
    def get(self, name):
        """Get major by name.

        Parameters
        ----------
        - name : [String]

        Returns
        -------
        [JSON]
            dict with the structure:
            {
                "major": {
                    "name": name,
                    "code": code,
                }
            }
        """
        major = major_dao.get_by_name(name=name)
        if major:
            return major_schema.dump(major)

        api.abort(404, message="The major was not found.",
                  status="Could not find information", statusCode="404")
