from alfred.schemas.departments import DepartmentSchema
from alfred.dao.departments import department_dao
from alfred.services.departments import department_service

from flask_restx import Namespace, Resource, reqparse


api = Namespace('departments', description='Department-related operations')
department_schema = DepartmentSchema()


@api.route('/all')
@api.response('200', 'Success')
class Departments(Resource):
    def get(self):
        """An endpoint to get all departments from the database.

        Parameters
        ----------
        None

        Returns
        -------
        [JSON]
            dict of the form {"departments": [list-of-departments]}
        """
        all_departments = department_dao.get_all()
        return department_schema.dump(all_departments, many=True)


parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('code', required=True)


@api.route('/add')
@api.response('201', 'Success: The department was created successfully.')
@api.response('400', 'Error: Bad request. Check parameters.')
@api.response('422', 'Error: The request failed.')
class AddDepartment(Resource):
    """Resource to add a new department.
    """
    @api.expect(parser)
    def post(self):
        """Add a new department.

        Parameters
        ----------
        - name:
            department name has to be unique.
        - code:
            department's code has to be unique.
        """
        args = parser.parse_args()
        name = args['name']
        code = args['code']

        if name and code:
            try:
                department_service.create_department(name=name, code=code)
                return "The department was created successfully.", 201
            except Exception as e:
                api.abort(422, e, status="Could not save information",
                          statusCode="422")


@api.route('/<int:department_id>')
@api.param('department_id', 'Department identifier', required=True)
@api.response('200', 'Success: Department found.')
@api.response('404', 'Error: Department not found.')
class getDepartment(Resource):
    """Resource to get a department by their ID.
    """
    def get(self, department_id):
        """Get department by id.

        Parameters
        ----------
        - department_id : [int]

        Returns
        -------
        [JSON]
            dict with the structure:
            {
                "department": {
                    "name": name,
                    "code": code,
                }
            }
        """
        department = department_dao.get_by_id(department_id=department_id)
        if department:
            return department_schema.dump(department)

        api.abort(404, message="The department was not found.",
                  status="Could not find information", statusCode="404")


@api.route('/<name>')
@api.param('name', required=True)
@api.response('200', 'Success: Department found.')
@api.response('404', 'Error: Department not found.')
class getDepartmentName(Resource):
    """Resource to get a department by their name.
    """
    def get(self, name):
        """Get department by name.

        Parameters
        ----------
        - name : [String]

        Returns
        -------
        [JSON]
            dict with the structure:
            {
                "department": {
                    "name": name,
                    "code": code,
                }
            }
        """
        department = department_dao.get_by_name(name=name)
        if department:
            return department_schema.dump(department)

        api.abort(404, message="The department was not found.",
                  status="Could not find information", statusCode="404")
