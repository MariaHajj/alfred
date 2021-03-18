from alfred.schemas.petition_types import PetitionTypeSchema
from alfred.dao.petition_types import petition_type_dao
from alfred.services.petition_types import petition_type_service

from flask_restx import Namespace, Resource, reqparse


api = Namespace('petition_types',
                description='Petition Type-related operations')
petition_type_schema = PetitionTypeSchema()


@api.route('/all')
@api.response('200', 'Success')
class PetitionTypes(Resource):
    def get(self):
        """An endpoint to get all petition types from the database.

        Parameters
        ----------
        None

        Returns
        -------
        [JSON]
            dict of the form {"petition_types": [list-of-petition_type]}
        """
        all_petition_types = petition_type_dao.get_all()
        return petition_type_schema.dump(all_petition_types, many=True)


parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('description', required=True)


@api.route('/add')
@api.response('201', 'Success: The petition type was created successfully.')
@api.response('400', 'Error: Bad request. Check parameters.')
@api.response('422', 'Error: The request failed.')
class AddPetitionType(Resource):
    """Resource to add a new petition type.
    """
    @api.expect(parser)
    def post(self):
        """Add a new petition type.

        Parameters
        ----------
        - name:
            petition type name has to be unique.
        - description:
            petition type's description has to be unique.
        """
        args = parser.parse_args()
        name = args['name']
        description = args['description']

        if name and description:
            try:
                petition_type_service\
                    .create_petition_type(name=name, description=description)
                return "The petition type was created successfully.", 201
            except Exception as e:
                api.abort(422, e, status="Could not save information",
                          statusCode="422")


@api.route('/<int:petition_type_id>')
@api.param('petition_type_id', 'Petition type identifier', required=True)
@api.response('200', 'Success: Petition type found.')
@api.response('404', 'Error: Petition type not found.')
class getPetitionType(Resource):
    """Resource to get a petition type by their ID.
    """
    def get(self, petition_type_id):
        """Get petition type by id.

        Parameters
        ----------
        - petition_type_id : [int]

        Returns
        -------
        [JSON]
            dict with the structure:
            {
                "petition_type": {
                    "name": name,
                    "description": description,
                }
            }
        """
        petition_type = petition_type_dao\
            .get_by_id(petition_type_id=petition_type_id)
        if petition_type:
            return petition_type_schema.dump(petition_type)

        api.abort(404, message="The petition type was not found.",
                  status="Could not find information", statusCode="404")


@api.route('/<name>')
@api.param('name', required=True)
@api.response('200', 'Success: Petiton type found.')
@api.response('404', 'Error: Petition type not found.')
class getPetitionTypeName(Resource):
    """Resource to get a petition type by their name.
    """
    def get(self, name):
        """Get petition type by name.

        Parameters
        ----------
        - name : [String]

        Returns
        -------
        [JSON]
            dict with the structure:
            {
                "petition_type": {
                    "name": name,
                    "description": description,
                }
            }
        """
        petition_type = petition_type_dao.get_by_name(name=name)
        if petition_type:
            return petition_type_schema.dump(petition_type)

        api.abort(404, message="The petition type was not found.",
                  status="Could not find information", statusCode="404")
