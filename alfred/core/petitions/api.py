from alfred.schemas.petitions import PetitionSchema
from alfred.dao.petitions import petition_dao
from alfred.services.petitions import petition_service

from flask_restx import Namespace, Resource, reqparse
from flask_restful import inputs


api = Namespace('petitions', description='Petition-related operations')
petition_schema = PetitionSchema()


@api.route('/all')
@api.response('200', 'Success')
class Petitions(Resource):
    def get(self):
        """An endpoint to get all petitions from the database.

        Parameters
        ----------
        None

        Returns
        -------
        [JSON]
            dict of the form {"petitions": [list-of-petitions]}
        """
        all_petitions = petition_dao.get_all()
        return petition_schema.dump(all_petitions, many=True)


parser = reqparse.RequestParser()
parser.add_argument('transcript', required=True)
parser.add_argument('request_comment', required=True)
parser.add_argument('date_submitted: YYYY-MM-DD',
                    type=inputs.date, required=True)
parser.add_argument('advisor_comment', required=True)
parser.add_argument('decision_comment', required=True)
parser.add_argument('date_decided: YYYY-MM-DD',
                    type=inputs.date, required=True)


@api.route('/add')
@api.response('201', 'Success: The petition was created successfully.')
@api.response('400', 'Error: Bad request. Check parameters.')
@api.response('422', 'Error: The request failed.')
class AddPetition(Resource):
    """Resource to add a new petition.
    """
    @api.expect(parser)
    def post(self):
        """Add a new petition.

        Parameters
        ----------
        - transcript, request_comment, date_submitted, advisor_comment,
          decision_comment, date_decided
        """
        args = parser.parse_args()
        transcript = args['transcript']
        request_comment = args['request_comment']
        date_submitted = args['date_submitted: YYYY-MM-DD']
        advisor_comment = args['advisor_comment']
        decision_comment = args['decision_comment']
        date_decided = args['date_decided: YYYY-MM-DD']

        if transcript and request_comment and date_submitted and\
           advisor_comment and decision_comment and date_decided:
            try:
                petition_service\
                    .create_petition(transcript=transcript,
                                     request_comment=request_comment,
                                     date_submitted=date_submitted,
                                     advisor_comment=advisor_comment,
                                     decision_comment=decision_comment,
                                     date_decided=date_decided)
                return "The petition was created successfully.", 201
            except Exception as e:
                api.abort(422, e, status="Could not save information",
                          statusCode="422")


@api.route('/<int:petition_id>')
@api.param('petition_id', 'Petition identifier', required=True)
@api.response('200', 'Success: Petition found.')
@api.response('404', 'Error: Petition not found.')
class getPetition(Resource):
    """Resource to get a petition by their ID.
    """
    def get(self, petition_id):
        """Get petition by id.

        Parameters
        ----------
        - petition_id : [int]

        Returns
        -------
        [JSON]
            dict with the structure:
            {
                "petition": {
                    "transcript": transcript,
                    "request_comment": request_comment,
                    "date_submitted": date_submitted,
                    "advisor_comment": advisor_comment,
                    "decision_comment": decision_comment,
                    "date_decided": date_decided,
                }
            }
        """
        petition = petition_dao.get_by_id(petition_id=petition_id)
        if petition:
            return petition_schema.dump(petition)

        api.abort(404, message="The petition was not found.",
                  status="Could not find information", statusCode="404")
