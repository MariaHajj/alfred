from alfred.schemas.users import UserSchema
from alfred.dao.users import user_dao
from alfred.services.users import user_service

from flask_restx import Namespace, Resource, reqparse


api = Namespace('users', description='User-related operations')
user_schema = UserSchema()


@api.route('/all')
@api.response('200', 'Success')
class Users(Resource):
    def get(self):
        """An endpoint to get all users from the database.

        Parameters
        ----------
        None

        Returns
        -------
        [JSON]
            dict of the form {"users": [list-of-users]}
        """
        all_users = user_dao.get_all()
        return user_schema.dump(all_users, many=True)


parser = reqparse.RequestParser()
parser.add_argument('aub_id', required=True)
parser.add_argument('email', required=True)
parser.add_argument('first_name', required=True)
parser.add_argument('last_name', required=True)
parser.add_argument('major', required=True)
parser.add_argument('password', required=True)


@api.route('/add')
@api.response('201', 'Success: The user was created successfully.')
@api.response('400', 'Error: Bad request. Check parameters.')
@api.response('422', 'Error: The request failed.')
class AddUser(Resource):
    """Resource to add a new user.
    """
    @api.expect(parser)
    def post(self):
        """Add a new user.

        Parameters
        ----------
        - aub_id:
            AUB IDs have to be unique.
        - first_name, last_name, and major
        - email:
            Emails have to be unique.
        - password:
            Passwords are automatically hashed when they are stored.
        """
        args = parser.parse_args()
        aub_id = args['aub_id']
        email = args['email']
        first_name = args['first_name']
        last_name = args['last_name']
        major = args['major']
        password = args['password']

        if aub_id and \
           email and \
           first_name and \
           last_name and \
           major and \
           password:
            try:
                user_service.create_user(aub_id=aub_id,
                                         email=email,
                                         first_name=first_name,
                                         last_name=last_name,
                                         major=major,
                                         password=password)
                return "The user was created successfully.", 201
            except Exception as e:
                api.abort(422, e, status="Could not save information",
                          statusCode="422")


@api.route('/<int:user_id>')
@api.param('user_id', 'User identifier', required=True)
@api.response('200', 'Success: User found.')
@api.response('404', 'Error: User not found.')
class getUser(Resource):
    """Resource to get a user by their ID.
    """
    def get(self, user_id):
        """Get user by id.

        Parameters
        ----------
        - user_id : [int]

        Returns
        -------
        [JSON]
            dict with the structure:
            {
                "user": {
                    "aub_id": aub_id,
                    "email": email,
                    "first_name": first_name,
                    "last_name": last_name,
                    "password": hashed password,
                    "image_path": name of profile picture
                }
            }
        """
        user = user_dao.get_by_id(user_id=user_id)
        if user:
            return user_schema.dump(user)

        api.abort(404, message="The user was not found.",
                  status="Could not find information", statusCode="404")
