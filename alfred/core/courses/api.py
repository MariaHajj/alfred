from alfred.schemas.courses import CourseSchema
from alfred.dao.courses import course_dao
from alfred.services.courses import course_service

from flask_restx import Namespace, Resource, reqparse
from flask_restful import inputs


api = Namespace('courses', description='Course-related operations')
course_schema = CourseSchema()


@api.route('/all')
@api.response('200', 'Success')
class Courses(Resource):
    def get(self):
        """An endpoint to get all courses from the database.

        Parameters
        ----------
        None

        Returns
        -------
        [JSON]
            dict of the form {"courses": [list-of-courses]}
        """
        all_courses = course_dao.get_all()
        return course_schema.dump(all_courses, many=True)


parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('description', required=True)
parser.add_argument('course code (ex: CMPS)', required=True)
parser.add_argument('number', type=inputs.positive, required=True)


@api.route('/add')
@api.response('201', 'Success: The course was created successfully.')
@api.response('400', 'Error: Bad request. Check parameters.')
@api.response('422', 'Error: The request failed.')
class AddCourse(Resource):
    """Resource to add a new course.
    """
    @api.expect(parser)
    def post(self):
        """Add a new course.

        Parameters
        ----------
        - name:
            course name has to be unique.
        - description.
        - code:
            course's code
        - number:
            course's number has to be unique.
        """
        args = parser.parse_args()
        name = args['name']
        description = args['description']
        code = args['course code (ex: CMPS)']
        number = args['number']

        if name and description and code and number:
            try:
                course_service.create_course(name=name,
                                             description=description,
                                             code=code.upper(),
                                             number=int(number))
                return "The course was created successfully.", 201
            except Exception as e:
                api.abort(422, e, status="Could not save information",
                          statusCode="422")


@api.route('/<int:course_id>')
@api.param('course_id', 'Course identifier', required=True)
@api.response('200', 'Success: Course found.')
@api.response('404', 'Error: Course not found.')
class getCourse(Resource):
    """Resource to get a course by their ID.
    """
    def get(self, course_id):
        """Get course by id.

        Parameters
        ----------
        - course_id : [int]

        Returns
        -------
        [JSON]
            dict with the structure:
            {
                "course": {
                    "name": name,
                    "description": description,
                    "code": code,
                    "number": number,
                }
            }
        """
        course = course_dao.get_by_id(course_id=course_id)
        if course:
            return course_schema.dump(course)

        api.abort(404, message="The course was not found.",
                  status="Could not find information", statusCode="404")


@api.route('/<name>')
@api.param('name', required=True)
@api.response('200', 'Success: Course found.')
@api.response('404', 'Error: Course not found.')
class getCourseName(Resource):
    """Resource to get a course by their name.
    """
    def get(self, name):
        """Get course by name.

        Parameters
        ----------
        - name : [String]

        Returns
        -------
        [JSON]
            dict with the structure:
            {
                "course": {
                    "name": name,
                    "description": description,
                    "code": code,
                    "number": number,
                }
            }
        """
        course = course_dao.get_by_name(name=name)
        if course:
            return course_schema.dump(course)

        api.abort(404, message="The course was not found.",
                  status="Could not find information", statusCode="404")


@api.route('/<code>')
@api.param('code', required=True)
@api.response('200', 'Success: Course found.')
@api.response('404', 'Error: Course not found.')
class getCourseCode(Resource):
    """Resource to get a course by their letter code.
    """
    def get(self, code):
        """Get course by code.

        Parameters
        ----------
        - code : [string]

        Returns
        -------
        [JSON]
            dict with the structure:
            {
                "course": {
                    "name": name,
                    "description": description,
                    "code": code,
                    "number": number,
                }
            }
        """
        course = course_dao.get_by_code(code=code)
        if course:
            return course_schema.dump(course)

        api.abort(404, message="The course was not found.",
                  status="Could not find information", statusCode="404")


@api.route('/<number>')
@api.param('number', required=True)
@api.response('200', 'Success: Course found.')
@api.response('404', 'Error: Course not found.')
class getCourseNumber(Resource):
    """Resource to get a course by their number.
    """
    def get(self, number):
        """Get course by number.

        Parameters
        ----------
        - number : [int]

        Returns
        -------
        [JSON]
            dict with the structure:
            {
                "course": {
                    "name": name,
                    "description": description,
                    "code": code,
                    "number": number,
                }
            }
        """
        course = course_dao.get_by_number(number=number)
        if course:
            return course_schema.dump(course)

        api.abort(404, message="The course was not found.",
                  status="Could not find information", statusCode="404")
