from alfred.schemas.announcements import AnnouncementSchema
from alfred.dao.announcements import announcement_dao
from alfred.services.announcements import announcement_service

from flask_restx import Namespace, Resource, reqparse


api = Namespace('announcements', description='Announcement-related operations')
announcement_schema = AnnouncementSchema()


@api.route('/all')
@api.response('200', 'Success')
class Announcements(Resource):
    def get(self):
        """An endpoint to get all announcements from the database.

        Parameters
        ----------
        None

        Returns
        -------
        [JSON]
            dict of the form {"announcements": [list-of-announcements]}
        """
        all_announcements = announcement_dao.get_all()
        return announcement_schema.dump(all_announcements, many=True)


parser = reqparse.RequestParser()
parser.add_argument('title', required=True)
parser.add_argument('description', required=True)


@api.route('/add')
@api.response('201', 'Success: The announcement was created successfully.')
@api.response('400', 'Error: Bad request. Check parameters.')
@api.response('422', 'Error: The request failed.')
class AddAnnouncement(Resource):
    """Resource to add a new announcement.
    """
    @api.expect(parser)
    def post(self):
        """Add a new announcement.

        Parameters
        ----------
        - title, description.
        """
        args = parser.parse_args()
        title = args['title']
        description = args['description']

        if title and description:
            try:
                announcement_service\
                    .create_announcement(title=title, description=description)
                return "The announcement was created successfully.", 201
            except Exception as e:
                api.abort(422, e, status="Could not save information",
                          statusCode="422")


@api.route('/<int:announcement_id>')
@api.param('announcement_id', 'Announcement identifier', required=True)
@api.response('200', 'Success: Announcement found.')
@api.response('404', 'Error: Announcement not found.')
class getAnnouncement(Resource):
    """Resource to get a announcement by their ID.
    """
    def get(self, announcement_id):
        """Get announcement by id.

        Parameters
        ----------
        - announcement_id : [int]

        Returns
        -------
        [JSON]
            dict with the structure:
            {
                "announcement": {
                    "title": title,
                    "description": description,
                }
            }
        """
        announcement = announcement_dao\
            .get_by_id(announcement_id=announcement_id)
        if announcement:
            return announcement_schema.dump(announcement)

        api.abort(404, message="The announcement was not found.",
                  status="Could not find information", statusCode="404")
