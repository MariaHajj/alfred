from alfred.schemas.frequencies import FrequencySchema
from alfred.dao.frequencies import frequency_dao
from alfred.services.frequencies import frequency_service

from flask_restx import Namespace, Resource, reqparse


api = Namespace('frequencies', description='Frequency-related operations')
frequency_schema = FrequencySchema()


@api.route('/all')
@api.response('200', 'Success')
class Frequencies(Resource):
    def get(self):
        """An endpoint to get all frequencies from the database.

        Parameters
        ----------
        None

        Returns
        -------
        [JSON]
            dict of the form {"frequencies": [list-of-frequencies]}
        """
        all_frequencies = frequency_dao.get_all()
        return frequency_schema.dump(all_frequencies, many=True)


parser = reqparse.RequestParser()
parser.add_argument('value', required=True)
parser.add_argument('description', required=True)


@api.route('/add')
@api.response('201', 'Success: The frequency was created successfully.')
@api.response('400', 'Error: Bad request. Check parameters.')
@api.response('422', 'Error: The request failed.')
class AddFrequency(Resource):
    """Resource to add a new frequency.
    """
    @api.expect(parser)
    def post(self):
        """Add a new frequency.

        Parameters
        ----------
        - value:
            frequency value has to be unique.
        - description.
        """
        args = parser.parse_args()
        value = args['value']
        description = args['description']

        if value and description:
            try:
                frequency_service.create_frequency(value=value,
                                                   description=description)
                return "The frequency was created successfully.", 201
            except Exception as e:
                api.abort(422, e, status="Could not save information",
                          statusCode="422")


@api.route('/<int:frequency_id>')
@api.param('frequency_id', 'Frequency identifier', required=True)
@api.response('200', 'Success: Frequency found.')
@api.response('404', 'Error: Frequency not found.')
class getFrequency(Resource):
    """Resource to get a frequency by their ID.
    """
    def get(self, frequency_id):
        """Get frequency by id.

        Parameters
        ----------
        - frequency_id : [int]

        Returns
        -------
        [JSON]
            dict with the structure:
            {
                "frequency": {
                    "value": value,
                    "description": description,
                }
            }
        """
        frequency = frequency_dao.get_by_id(frequency_id=frequency_id)
        if frequency:
            return frequency_schema.dump(frequency)

        api.abort(404, message="The frequency was not found.",
                  status="Could not find information", statusCode="404")


@api.route('/<value>')
@api.param('value', required=True)
@api.response('200', 'Success: Frequency found.')
@api.response('404', 'Error: Frequency not found.')
class getFrequencyValue(Resource):
    """Resource to get a frequency by their value.
    """
    def get(self, value):
        """Get frequency by value.

        Parameters
        ----------
        - value : [String]

        Returns
        -------
        [JSON]
            dict with the structure:
            {
                "frequency": {
                    "value": value,
                    "description": description,
                }
            }
        """
        frequency = frequency_dao.get_by_value(value=value)
        if frequency:
            return frequency_schema.dump(frequency)

        api.abort(404, message="The frequency was not found.",
                  status="Could not find information", statusCode="404")
