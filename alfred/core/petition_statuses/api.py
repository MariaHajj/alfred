from alfred.schemas.petition_statuses import PetitionStatusSchema
from alfred.dao.petition_statuses import petition_status_dao
from alfred.services.petition_statuses import petition_status_service

from flask_restx import Namespace, Resource, reqparse


api = Namespace('petition_statuses',
                description='Petition Status-related operations')
petition_status_schema = PetitionStatusSchema()


@api.route('/all')
@api.response('200', 'Success')
class PetitionStatuses(Resource):
    def get(self):
        """An endpoint to get all petition statuses from the database.

        Parameters
        ----------
        None

        Returns
        -------
        [JSON]
            dict of the form {"petition_statuses": [list-of-petition_statuses]}
        """
        all_petition_statuses = petition_status_dao.get_all()
        return petition_status_schema.dump(all_petition_statuses, many=True)


parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('description', required=True)


@api.route('/add')
@api.response('201', 'Success: The petition status was created successfully.')
@api.response('400', 'Error: Bad request. Check parameters.')
@api.response('422', 'Error: The request failed.')
class AddPetitionStatus(Resource):
    """Resource to add a new petition status.
    """
    @api.expect(parser)
    def post(self):
        """Add a new petition status.

        Parameters
        ----------
        - name:
            petition status name has to be unique.
        - description:
            petition status's description has to be unique.
        """
        args = parser.parse_args()
        name = args['name']
        description = args['description']

        if name and description:
            try:
                petition_status_service\
                    .create_petition_status(name=name, description=description)
                return "The petition status was created successfully.", 201
            except Exception as e:
                api.abort(422, e, status="Could not save information",
                          statusCode="422")


@api.route('/<int:petition_status_id>')
@api.param('petition_status_id', 'Petition status identifier', required=True)
@api.response('200', 'Success: Petition status found.')
@api.response('404', 'Error: Petition status not found.')
class getPetitionStatus(Resource):
    """Resource to get a petition status by their ID.
    """
    def get(self, petition_status_id):
        """Get petition status by id.

        Parameters
        ----------
        - petition_status_id : [int]

        Returns
        -------
        [JSON]
            dict with the structure:
            {
                "petition_status": {
                    "name": name,
                    "description": description,
                }
            }
        """
        petition_status = petition_status_dao\
            .get_by_id(petition_status_id=petition_status_id)
        if petition_status:
            return petition_status_schema.dump(petition_status)

        api.abort(404, message="The petition status was not found.",
                  status="Could not find information", statusCode="404")


@api.route('/<name>')
@api.param('name', required=True)
@api.response('200', 'Success: Petiton status found.')
@api.response('404', 'Error: Petition status not found.')
class getPetitionStatusName(Resource):
    """Resource to get a petition status by their name.
    """
    def get(self, name):
        """Get petition status by name.

        Parameters
        ----------
        - name : [String]

        Returns
        -------
        [JSON]
            dict with the structure:
            {
                "petition_status": {
                    "name": name,
                    "description": description,
                }
            }
        """
        petition_status = petition_status_dao.get_by_name(name=name)
        if petition_status:
            return petition_status_schema.dump(petition_status)

        api.abort(404, message="The petition status was not found.",
                  status="Could not find information", statusCode="404")
