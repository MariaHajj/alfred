from alfred.schemas.faculties import FacultySchema
from alfred.dao.faculties import faculty_dao
from alfred.services.faculties import faculty_service

from flask_restx import Namespace, Resource, reqparse


api = Namespace('faculties', description='Faculty-related operations')
faculty_schema = FacultySchema()


@api.route('/all')
@api.response('200', 'Success')
class Faculties(Resource):
    def get(self):
        """An endpoint to get all faculties from the database.

        Parameters
        ----------
        None

        Returns
        -------
        [JSON]
            dict of the form {"faculties": [list-of-faculties]}
        """
        all_faculties = faculty_dao.get_all()
        return faculty_schema.dump(all_faculties, many=True)


parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('code', required=True)


@api.route('/add')
@api.response('201', 'Success: The faculty was created successfully.')
@api.response('400', 'Error: Bad request. Check parameters.')
@api.response('422', 'Error: The request failed.')
class AddFaculty(Resource):
    """Resource to add a new faculty.
    """
    @api.expect(parser)
    def post(self):
        """Add a new faculty.

        Parameters
        ----------
        - name:
            faculty name has to be unique.
        - code:
            faculty's code has to be unique.
        """
        args = parser.parse_args()
        name = args['name']
        code = args['code']

        if name and code:
            try:
                faculty_service.create_faculty(name=name, code=code)
                return "The faculty was created successfully.", 201
            except Exception as e:
                api.abort(422, e, status="Could not save information",
                          statusCode="422")


@api.route('/<int:faculty_id>')
@api.param('faculty_id', 'Faculty identifier', required=True)
@api.response('200', 'Success: Faculty found.')
@api.response('404', 'Error: Faculty not found.')
class getFaculty(Resource):
    """Resource to get a faculty by their ID.
    """
    def get(self, faculty_id):
        """Get faculty by id.

        Parameters
        ----------
        - faculty_id : [int]

        Returns
        -------
        [JSON]
            dict with the structure:
            {
                "faculty": {
                    "name": name,
                    "code": code,
                }
            }
        """
        faculty = faculty_dao.get_by_id(faculty_id=faculty_id)
        if faculty:
            return faculty_schema.dump(faculty)

        api.abort(404, message="The faculty was not found.",
                  status="Could not find information", statusCode="404")


@api.route('/<name>')
@api.param('name', required=True)
@api.response('200', 'Success: Faculty found.')
@api.response('404', 'Error: Faculty not found.')
class getFacultyName(Resource):
    """Resource to get a faculty by their name.
    """
    def get(self, name):
        """Get faculty by name.

        Parameters
        ----------
        - name : [String]

        Returns
        -------
        [JSON]
            dict with the structure:
            {
                "faculty": {
                    "name": name,
                    "code": code,
                }
            }
        """
        faculty = faculty_dao.get_by_name(name=name)
        if faculty:
            return faculty_schema.dump(faculty)

        api.abort(404, message="The faculty was not found.",
                  status="Could not find information", statusCode="404")
