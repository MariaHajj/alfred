from alfred.models import Petition
from alfred import db


class PetitionDAO():
    """Class to handle all database operations
    for models.Petition class.
    """
    __instance__ = None

    def __init__(self):
        if PetitionDAO.__instance__ is None:
            PetitionDAO.__instance__ = self
        else:
            raise Exception("You cannot create another PetitionDAO class")

    @staticmethod
    def get_instance():
        if not PetitionDAO.__instance__:
            PetitionDAO()
        return PetitionDAO.__instance__

    def add(self, petition):
        db.session.add(petition)
        db.session.commit()

    def get_all(self):
        return db.session.query(Petition).all()

    def get_by_id(self, petition_id):
        return db.session.query(Petition).get(petition_id)

    def get_by_user(self, user):
        return db.session.query(Petition).filter_by(user=user).all()

    def get_total_num(self, user):
        return db.session.query(Petition).filter_by(user=user).count()

    def delete_petition_by_id(self, petition_id):
        db.session.query(Petition).filter_by(id=petition_id).delete()
        db.session.commit()


petition_dao = PetitionDAO.get_instance()
