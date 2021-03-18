from alfred.schemas.terms import TermSchema
from alfred.dao.terms import term_dao
from alfred.services.terms import term_service

from flask_restx import Namespace, Resource, reqparse
from flask_restful import inputs


api = Namespace('terms', description='Term-related operations')
term_schema = TermSchema()


@api.route('/all')
@api.response('200', 'Success')
class Terms(Resource):
    def get(self):
        """An endpoint to get all terms from the database.

        Parameters
        ----------
        None

        Returns
        -------
        [JSON]
            dict of the form {"terms": [list-of-terms]}
        """
        all_terms = term_dao.get_all()
        return term_schema.dump(all_terms, many=True)


parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('start_date: YYYY-MM-DD', type=inputs.date, required=True)
parser.add_argument('end_date: YYYY-MM-DD', type=inputs.date, required=True)


@api.route('/add')
@api.response('201', 'Success: The term was created successfully.')
@api.response('400', 'Error: Bad request. Check parameters.')
@api.response('422', 'Error: The request failed.')
class AddTerm(Resource):
    """Resource to add a new term.
    """
    @api.expect(parser)
    def post(self):
        """Add a new term.

        Parameters
        ----------
        - name:
            term name has to be unique.
        - start_date, end_date
        """
        args = parser.parse_args()
        name = args['name']
        start_date = args['start_date: YYYY-MM-DD']
        end_date = args['end_date: YYYY-MM-DD']

        if name and start_date and end_date:
            try:
                term_service.create_term(name=name, start_date=start_date,
                                         end_date=end_date)
                return "The term was created successfully.", 201
            except Exception as e:
                api.abort(422, e, status="Could not save information",
                          statusCode="422")


@api.route('/<int:term_id>')
@api.param('term_id', 'Term identifier', required=True)
@api.response('200', 'Success: Term found.')
@api.response('404', 'Error: Term not found.')
class getTerm(Resource):
    """Resource to get a term by their ID.
    """
    def get(self, term_id):
        """Get term by id.

        Parameters
        ----------
        - term_id : [int]

        Returns
        -------
        [JSON]
            dict with the structure:
            {
                "term": {
                    "name": name,
                    "start_date": start_date,
                    "end_date": end_date,
                }
            }
        """
        term = term_dao.get_by_id(term_id=term_id)
        if term:
            return term_schema.dump(term)

        api.abort(404, message="The term was not found.",
                  status="Could not find information", statusCode="404")


@api.route('/<name>')
@api.param('name', required=True)
@api.response('200', 'Success: Term found.')
@api.response('404', 'Error: Term not found.')
class getTermName(Resource):
    """Resource to get a term by their name.
    """
    def get(self, name):
        """Get term by name.

        Parameters
        ----------
        - name : [String]

        Returns
        -------
        [JSON]
            dict with the structure:
            {
                "term": {
                    "name": name,
                    "start_date": start_date,
                    "end_date": end_date,
                }
            }
        """
        term = term_dao.get_by_name(name=name)
        if term:
            return term_schema.dump(term)

        api.abort(404, message="The term was not found.",
                  status="Could not find information", statusCode="404")
