from alfred.models import Announcement
from alfred import db
from sqlalchemy import desc


class AnnouncementDAO():
    """Class to handle all database operations
    for models.Announcement class.
    """
    __instance__ = None

    def __init__(self):
        if AnnouncementDAO.__instance__ is None:
            AnnouncementDAO.__instance__ = self
        else:
            raise Exception("You cannot create another AnnouncementDAO class")

    @staticmethod
    def get_instance():
        if not AnnouncementDAO.__instance__:
            AnnouncementDAO()
        return AnnouncementDAO.__instance__

    def add(self, announcement):
        db.session.add(announcement)
        db.session.commit()

    # get all ordered by date descending
    def get_all(self):
        return db.session.query(Announcement)\
            .order_by(desc(Announcement.upload_date)).all()

    def get_by_id(self, announcement_id):
        return db.session.query(Announcement).get(announcement_id)

    def get_by_title(self, title):
        return db.session.query(Announcement).filter_by(title=title).first()

    def delete_announcement_by_id(self, announcement_id):
        db.session.query(Announcement).filter_by(id=announcement_id).delete()
        db.session.commit()


announcement_dao = AnnouncementDAO.get_instance()
