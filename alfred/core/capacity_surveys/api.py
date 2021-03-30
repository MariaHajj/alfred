from alfred.schemas.capacity_surveys import CapacitySurveySchema
from alfred.dao.capacity_surveys import capacity_survey_dao
from alfred.services.capacity_surveys import capacity_survey_service

from flask_restx import Namespace, Resource, reqparse, inputs


api = Namespace('surveys',
                description='Survey-related operations')
capacity_survey_schema = CapacitySurveySchema()


@api.route('/all')
@api.response('200', 'Success')
class CapacitySurveys(Resource):
    def get(self):
        """An endpoint to get all capacity surveys from the database.

        Parameters
        ----------
        None

        Returns
        -------
        [JSON]
            dict of the form {"capacity_surveys": [list-of-capacity_surveys]}
        """
        all_capacity_surveys = capacity_survey_dao.get_all()
        return capacity_survey_schema.dump(all_capacity_surveys, many=True)


parser = reqparse.RequestParser()
parser.add_argument('title', required=True)
parser.add_argument('start_date: YYYY-MM-DD', type=inputs.date,
                    required=True)
parser.add_argument('end_date: YYYY-MM-DD', type=inputs.date,
                    required=True)
parser.add_argument('comment', required=True)


@api.route('/add')
@api.response('201', 'Success: The capacity survey was created successfully.')
@api.response('400', 'Error: Bad request. Check parameters.')
@api.response('422', 'Error: The request failed.')
class AddCapacitySurvey(Resource):
    """Resource to add a new capacity survey.
    """
    @api.expect(parser)
    def post(self):
        """Add a new capacity survey.

        Parameters
        ----------
        - title, start_date, end_date, number_of_requests, comment.
        """
        args = parser.parse_args()
        title = args['title']
        start_date = args['start_date: YYYY-MM-DD']
        end_date = args['end_date: YYYY-MM-DD']
        comment = args['comment']

        if title and start_date and end_date and comment:
            try:
                capacity_survey_service\
                    .create_capacity_survey(title=title,
                                            start_date=start_date,
                                            end_date=end_date,
                                            comment=comment)
                return "The capacity survey was created successfully.", 201
            except Exception as e:
                api.abort(422, e, status="Could not save information",
                          statusCode="422")


@api.route('/<int:capacity_survey_id>')
@api.param('capacity_survey_id', 'Capacity Survey identifier', required=True)
@api.response('200', 'Success: Capacity Survey found.')
@api.response('404', 'Error: Capacity survey not found.')
class getCapacitySurvey(Resource):
    """Resource to get a capacity survey by their ID.
    """
    def get(self, capacity_survey_id):
        """Get capacity survey by id.

        Parameters
        ----------
        - capacity_survey_id : [int]

        Returns
        -------
        [JSON]
            dict with the structure:
            {
                "capacity_survey": {
                    "title": title,
                    "start_date": start_date,
                    "end_date": end_date,
                    "number_of_requests": number_of_requests,
                    "comment": comment,
                }
            }
        """
        capacity_survey = capacity_survey_dao\
            .get_by_id(capacity_survey_id=capacity_survey_id)
        if capacity_survey:
            return capacity_survey_schema.dump(capacity_survey)

        api.abort(404, message="The capacity survey was not found.",
                  status="Could not find information", statusCode="404")
